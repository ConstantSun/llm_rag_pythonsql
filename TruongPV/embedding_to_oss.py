
import sys
sys.path.append("..")
import env
#import warnings
#warnings.filterwarnings('ignore')
import os
import boto3
import json
import numpy as np
from typing import Dict, List
from langchain.embeddings import SagemakerEndpointEmbeddings, BedrockEmbeddings
from langchain.embeddings.sagemaker_endpoint import EmbeddingsContentHandler
from langchain.llms.bedrock import Bedrock
from langchain.load.dump import dumps
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader,TextLoader
from langchain.document_loaders.csv_loader import CSVLoader

sbert_endpoint = env.embedding_enpoint
host = env.aos_endpoint

index_name = "questiontype"
module_path = ".."
sys.path.append(os.path.abspath(module_path))
import bedrock

os.environ["AWS_DEFAULT_REGION"] = env.region_name

boto3_bedrock = bedrock.get_bedrock_client(
    #assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
    region=os.environ.get("AWS_DEFAULT_REGION", None)
)

# - create the Anthropic Model
llm = Bedrock(
    model_id="anthropic.claude-v2", client=boto3_bedrock, model_kwargs={"max_tokens_to_sample": 200}
)

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

content_handler = ContentHandler()

sbert_batch_embeddings = SagemakerEndpointEmbeddings(
    # credentials_profile_name="credentials-profile-name",
    endpoint_name=sbert_endpoint, # change this to your own sbert endpoint
    region_name=env.region_name,  # change this to your sagemaker deployed sbert endpoint Region 
    content_handler=content_handler,
)

loader = CSVLoader("./Data/questiontype.csv", encoding = 'UTF-8')
documents = loader.load()

# - in our testing Character split works better with this PDF data set
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size= 1790 , #  because sbert 'max_seq_length': 256 ~ 70%*256 = 179 VN words -> *5 ->  895 chunk_size (characters)
    chunk_overlap= 150, # 70 ~ 14 words, one line.
)
docs = text_splitter.split_documents(documents)

from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from langchain.vectorstores import OpenSearchVectorSearch

import langchain 

service = 'aoss'
credentials = boto3.Session().get_credentials()
auth = AWSV4SignerAuth(credentials, os.environ.get("AWS_DEFAULT_REGION", None), service)

docsearch = OpenSearchVectorSearch.from_documents(
    docs,
    sbert_batch_embeddings,
    bulk_size=1000,
    opensearch_url=host,
    http_auth=auth,
    timeout = 100,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection,
    index_name=index_name,
    engine="faiss",
)

print(docs)