import pyathena
import pandas as pd

conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
cursor = conn.cursor()

def get_result():
  try:
    query = """SELECT dtyyyymmdd, close 
              FROM absdb.v3 
              WHERE LOWER(ticker) LIKE LOWER('%ABB%')
              ORDER BY dtyyyymmdd DESC
              LIMIT 14"""

    df = pd.read_sql(query, conn)
    df = df.sort_values('dtyyyymmdd')

    ema = df['close'].iloc[0]
    N = len(df)
    for i in range(1, N):
      ema = (df['close'].iloc[i] - ema) * (2 / (N + 1)) + ema
    
    return [ema]

  except:
    return ["no query result"]
