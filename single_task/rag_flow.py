from langchain.embeddings import SagemakerEndpointEmbeddings
from langchain.embeddings.sagemaker_endpoint import EmbeddingsContentHandler
from langchain.vectorstores import OpenSearchVectorSearch
import langchain 
from langchain.load.dump import dumps
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain

from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3
from botocore.credentials import Credentials   

import json
from typing import Dict, List

from bedrock import get_llm_stream
from types import FunctionType


class ContentHandler(EmbeddingsContentHandler):
    content_type = "application/json"
    accepts = "application/json"
   
    def transform_input(self, inputs: list[str], model_kwargs: Dict) -> bytes:
        """
        Transforms the input into bytes that can be consumed by SageMaker endpoint.
        Args:
            inputs: List of input strings.
            model_kwargs: Additional keyword arguments to be passed to the endpoint.
        Returns:
            The transformed bytes input.
        """
        # Example: inference.py expects a JSON string with a "inputs" key:
        input_str = json.dumps({"inputs": inputs, **model_kwargs})  
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes) -> List[List[float]]:
        """
        Transforms the bytes output from the endpoint into a list of embeddings.
        Args:
            output: The bytes output from SageMaker endpoint.
        Returns:
            The transformed output - list of embeddings
        Note:
            The length of the outer list is the number of input strings.
            The length of the inner lists is the embedding dimension.
        """
        # Example: inference.py returns a JSON string with the list of
        # embeddings in a "vectors" key:
        response_json = json.loads(output.read().decode("utf-8"))
        return response_json["vectors"]


def ask_streaming_rag(streaming_callback: FunctionType, query: str)-> str:
    '''
    Param: 
        streaming_callback: FunctionType
        query: str

    Return: Answer for query, str.
    '''

    print(".......................ASK STREAMING RAG: ", query)

    content_handler = ContentHandler()
    infloatbase_batch_embeddings = SagemakerEndpointEmbeddings(
        # credentials_profile_name="credentials-profile-name",
        endpoint_name="huggingface-pytorch-inference-2023-11-17-04-03-54-290", # TODO: change this to your own sbert endpoint
        region_name="us-east-1",  #  TODO: change this to your sagemaker deployed sbert endpoint Region 
        content_handler=content_handler,
    )
    
    print("Infloat e5-base: ", infloatbase_batch_embeddings)
    service = 'aoss'


    # create an STS client object that represents a live connection to the 
    # STS service
    sts_client = boto3.client('sts')

    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    assumed_role_object=sts_client.assume_role(
        RoleArn="arn:aws:iam::628152409662:role/ec2-oregon-role",  # TODO: change to your own role.
        RoleSessionName="AssumeRoleSession1"
    )
    credentials=assumed_role_object['Credentials']
    creds = Credentials(credentials['AccessKeyId'], credentials['SecretAccessKey'], token=credentials['SessionToken'])



    auth = AWSV4SignerAuth(creds, "us-east-1", service)   # TODO: change your region
    index_name = "infloatbase"    # TODO: change your index_name
    docsearch = OpenSearchVectorSearch(
        "https://f4rkudrfg2b0fp2a8qhi.us-east-1.aoss.amazonaws.com:443",  # TODO: Change your AOS endpoint here
        index_name,
        infloatbase_batch_embeddings,
        http_auth=auth,
        timeout = 100,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection,
        engine="faiss"
    )       
       
    # results = docsearch.similarity_search(query, k=3)  # our search query  # return 3 most relevant docs
    # print(dumps(results, pretty=True))

    # RetrievalQAWithSourcesChain(llm=llm, )
    # qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())
    qa = RetrievalQA.from_chain_type(llm=get_llm_stream(streaming_callback), 
                                     chain_type="stuff", 
                                     retriever=docsearch.as_retriever(search_kwargs={'k': 5}),
                                     return_source_documents=False)
    print("---- RAG Query 1---- in file: ", query)
    # answer = qa.run(query)

    # TODO: Rewrite code to answer question from AOS, LLM -> answer 404: can not answer if can't, else answer: 200: answer
    # print("---- RAG Query 1 1---- in file: ", query)
    # print("---- RAG Answer---- in file: ")
    # print(query, "\n-\n", answer)
    return qa.run(query)

