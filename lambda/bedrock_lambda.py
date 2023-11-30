# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
"""Helper utilities for working with Amazon Bedrock """
# Python Built-Ins:
import os
from typing import Optional
import env
# External Dependencies:
import boto3
from botocore.config import Config


def get_bedrock_client(
    assumed_role: Optional[str] = None,
    region: Optional[str] = None,
    runtime: Optional[bool] = True,
):
    """Create a boto3 client for Amazon Bedrock, with optional configuration overrides

    Parameters
    ----------
    assumed_role :
        Optional ARN of an AWS IAM role to assume for calling the Bedrock service. If not
        specified, the current active credentials will be used.
    region :
        Optional name of the AWS Region in which the service should be called (e.g. "us-east-1").
        If not specified, AWS_REGION or AWS_DEFAULT_REGION environment variable will be used.
    runtime :
        Optional choice of getting different client to perform operations with the Amazon Bedrock service.
    """
    if region is None:
        target_region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION"))
    else:
        target_region = region

    print(f"Create new client\n  Using region: {target_region}")
    session_kwargs = {"region_name": target_region}
    client_kwargs = {**session_kwargs}

    profile_name = os.environ.get("AWS_PROFILE")
    if profile_name:
        print(f"  Using profile: {profile_name}")
        session_kwargs["profile_name"] = profile_name

    retry_config = Config(
        region_name=target_region,
        retries={
            "max_attempts": 10,
            "mode": "standard",
        },
    )
    session = boto3.Session(**session_kwargs)

    if assumed_role:
        print(f"  Using role: {assumed_role}", end='')
        sts = session.client("sts")
        response = sts.assume_role(
            RoleArn=str(assumed_role),
            RoleSessionName="langchain-llm-1"
        )
        print(" ... successful!")
        client_kwargs["aws_access_key_id"] = response["Credentials"]["AccessKeyId"]
        client_kwargs["aws_secret_access_key"] = response["Credentials"]["SecretAccessKey"]
        client_kwargs["aws_session_token"] = response["Credentials"]["SessionToken"]

    if runtime:
        service_name='bedrock-runtime'
    else:
        service_name='bedrock'

    bedrock_client = session.client(
        service_name=service_name,
        config=retry_config,
        **client_kwargs
    )

    print("boto3 Bedrock client successfully created!")
    print(bedrock_client._endpoint)
    return bedrock_client



from langchain.llms.bedrock import Bedrock
from langchain.load.dump import dumps
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from botocore.exceptions import ClientError

os.environ["AWS_DEFAULT_REGION"] = "us-east-1" # TODO: change to your region

boto3_bedrock = get_bedrock_client(
    #assumed_role=os.environ.get("BEDROCK_ASSUME_ROLE", None),
    region=env.region_name
)



def get_socket_client(event, aws_region):
    api_id = event.get("requestContext", {}).get("apiId")
    stage = event.get("requestContext", {}).get("stage")
    connection_id = event.get("requestContext", {}).get("connectionId")
    api_management_client = boto3.client(
        "apigatewaymanagementapi", endpoint_url=f"https://{api_id}.execute-api.{aws_region}.amazonaws.com/{stage}"
    )

    return api_management_client, connection_id

class WebsocketStreamingCallbackHandler(StreamingStdOutCallbackHandler):
    def __init__(self, client, connection_id):
        self.socket_client = client
        self.connection_id = connection_id

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        # print(token, end="", flush=True)

        try:
            self.socket_client.post_to_connection(
                Data=json.dumps({
                    "action": "typing",
                    "content": token
                }).encode("utf-8"),
                ConnectionId=self.connection_id
            )
        except ClientError:
            print("Couldn't post to connection %s.", self.connection_id)
        except self.socket_client.exceptions.GoneException:
            print("Connection %s is gone, removing.", self.connection_id)

api_management_client, connection_id = get_socket_client(event=None, aws_region = env.region_name)
stream_handler = WebsocketStreamingCallbackHandler(api_management_client, connection_id)

# - create the Anthropic Model
llm = Bedrock(
    model_id="anthropic.claude-v2", 
    client=boto3_bedrock, 
    model_kwargs={"max_tokens_to_sample": 900, "temperature": 0, "top_k": 30, "top_p": 0.1,},
    callbacks=[stream_handler] ,
    streaming=True,
)

# Processing RAG...
# End streaming...
api_management_client.post_to_connection(
    Data=json.dumps({"action": "end"}).encode("utf-8"), ConnectionId=connection_id
)


import json
brt = boto3_bedrock


def ask_direct(question: str) -> str:
    body = json.dumps({
        "prompt": f"\n\nHuman: {question}\n\nAssistant:",
        "max_tokens_to_sample": 900,
        "temperature": 0,
        "top_p": 0.1,
    })

    modelId = 'anthropic.claude-v2'
    accept = 'application/json'
    contentType = 'application/json'

    response = brt.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    response_body = json.loads(response.get('body').read())

    # text
    return (response_body.get('completion'))

def ask_short(question: str) -> str:
    body = json.dumps({
        "prompt": f"\n\nHuman: {question}\n\nAssistant:",
        "max_tokens_to_sample": 50,
        "temperature": 0,
        "top_p": 0.1,
    })

    modelId = 'anthropic.claude-v2'
    accept = 'application/json'
    contentType = 'application/json'

    response = brt.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    response_body = json.loads(response.get('body').read())

    # text
    return (response_body.get('completion'))    