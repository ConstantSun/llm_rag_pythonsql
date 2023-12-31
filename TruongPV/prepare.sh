pip install --no-build-isolation --force-reinstall \
    "boto3>=1.28.57" \
    "awscli>=1.29.57" \
    "botocore>=1.31.57"

pip install -U opensearch-py==2.3.1 langchain==0.0.309 "pypdf>=3.8,<4" \
    apache-beam \
    datasets \
    tiktoken

