region_name="us-east-1" # TODO: Change this to your region name
aws_access_key_id=None
aws_secret_access_key=None
athena_s3_bucket="s3://abst-test-athena-log/" # TODO: Change this to your Athena query s3 bucket name
top_k=10
# more variable
aos_endpoint='https://f4rkudrfg2b0fp2a8qhi.us-east-1.aoss.amazonaws.com:443'
embedding_enpoint = 'huggingface-pytorch-inference-2023-11-17-04-03-54-290'
rolearn='arn:aws:iam::628152409662:role/ec2-oregon-role'
dataupcom_db_name='absdb'
table_name='v3'