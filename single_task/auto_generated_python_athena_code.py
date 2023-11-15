import pandas as pd
from pyathena import connect

def get_result():
  conn = connect(aws_access_key_id=None, 
                aws_secret_access_key=None,
                s3_staging_dir='s3://abst-test-athena-log/', 
                region_name='us-east-1')
  
  cursor = conn.cursor()

  query = """
    SELECT dtyyyymmdd, close
    FROM absdb.v2 
    WHERE ticker = 'VCB'
    ORDER BY dtyyyymmdd DESC 
    LIMIT 14
  """

  df = pd.read_sql(query, conn)
  
  prev_close = 0
  ad = 0
  for _, row in df.iterrows():
    date, close = row
    change = close - prev_close
    if change > 0:
      ad += change
    prev_close = close

  return [ad]
  
result = get_result()
print("AD indicator for VCB:", result[0])
