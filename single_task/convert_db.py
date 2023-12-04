import re
import env
import single_task.dbtable_info as dbtable_info

def postgres_to_athena(code):

  # Replace psycopg2 import with pyathena
  code = re.sub(r'import psycopg2', 'import pyathena', code)

  # Replace psycopg2 connection with pyathena connection
  code = re.sub(r'psycopg2\.connect\(.*?\)',f'pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir=\'{env.athena_s3_bucket}\', region_name=\'{env.region_name}\')', code)

  # Replace postgres schema references with Athena schema
  code = re.sub(r'public\.', 'mydb.', code)

  # Add database name beside table name
  code = re.sub(rf'FROM {dbtable_info.table_name}', f'FROM {dbtable_info.dataupcom_db_name}.{dbtable_info.table_name}', code)
  code = re.sub(rf'from {dbtable_info.table_name}', f'FROM {dbtable_info.dataupcom_db_name}.{dbtable_info.table_name}', code)

  return code

