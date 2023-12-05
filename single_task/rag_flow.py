from langchain.embeddings import SagemakerEndpointEmbeddings
from langchain.embeddings.sagemaker_endpoint import EmbeddingsContentHandler
from langchain.vectorstores import OpenSearchVectorSearch
import langchain 
from langchain.load.dump import dumps
from langchain.chains import RetrievalQA
# from .retrieval_qa import RetrievalQA
from langchain import PromptTemplate

from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3
from botocore.credentials import Credentials   

import json
from typing import Dict, List
import env
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


# additional_promt = """\n<Note> Nếu như bạn không biết câu trả lời, hãy trả lời: "Đang xử lý ...", không bịa ra câu trả lời, chỉ trả lời bằng tiếng Việt Nam.  </Note>\n"""
additional_promt = """ """
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
        endpoint_name=env.embedding_enpoint, # TODO: change this to your own sbert endpoint
        region_name=env.region_name,  #  TODO: change this to your sagemaker deployed sbert endpoint Region 
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
        RoleArn=env.rolearn,  # TODO: change to your own role.
        RoleSessionName="AssumeRoleSession1"
    )
    credentials=assumed_role_object['Credentials']
    creds = Credentials(credentials['AccessKeyId'], credentials['SecretAccessKey'], token=credentials['SessionToken'])



    auth = AWSV4SignerAuth(creds, env.region_name, service)   # TODO: change your region
    index_name = "infloatbase"    # TODO: change your index_name
    docsearch = OpenSearchVectorSearch(
        env.aos_endpoint,  # TODO: Change your AOS endpoint here
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


    template = """
Sử dụng những nội dung dưới đây để trả lời câu hỏi ở cuối.

{context}

<note>
Bạn là trợ lý ảo của công ty chứng khoán An Bình. Nếu bạn không thể trả lời câu hỏi dựa trên thông tin ở trên, chỉ cần trả lời "..." và không cần giải thích gì thêm, không thêm bất kì lời nói nào.
</note>

Câu hỏi: {question} 
<note> Response without preamble </note>
"""

#     template = """
# Bạn là trợ lý ảo của công ty chứng khoán An Bình. Nếu ai đó hỏi bạn là ai hay chỉ nói câu "xin chào", hãy trả lời "Tôi là trợ lý ảo của công ty chứng khoán An Bình". Ngoài ra, sử dụng những nội dung dưới đây để trả lời câu hỏi ở cuối.
# Lưu ý, nếu bạn không thể trả lời câu hỏi dựa trên thông tin ở dưới đây, chỉ cần trả lời "..." và không cần giải thích gì thêm, không thêm bất kì lời nói nào.

# {context}

# <note>
# Nếu bạn không thể trả lời câu hỏi dựa trên thông tin ở trên, chỉ cần trả lời "..." và không cần giải thích gì thêm, không thêm bất kì lời nói nào.
# </note>

# Câu hỏi: {question}
# <note> Response without preamble </note>
# """

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=template,
    )

    qa = RetrievalQA.from_chain_type(
        llm=get_llm_stream(streaming_callback), 
        chain_type='stuff',
        retriever=docsearch.as_retriever(search_kwargs={'k': 3}),
        verbose=True,
        chain_type_kwargs={
            "verbose": True,
            "prompt": prompt,
            
        }
    )

    # import IPython ; IPython.embed()
    print("---- RAG Query 1---- in file: ", query)
    # answer = qa.run(query)

    # TODO: Rewrite code to answer question from AOS, LLM -> answer 404: can not answer if can't, else answer: 200: answer
    # print("---- RAG Query 1 1---- in file: ", query)
    # print("---- RAG Answer---- in file: ")
    # print(query, "\n-\n", answer)
    return qa.run(query)

