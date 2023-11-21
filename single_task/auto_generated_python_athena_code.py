import pyathena
import pandas as pd

def get_result():
  try:
    conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
    cursor = conn.cursor()
    
    query = '''SELECT LOWER(ticker), close 
              FROM absdb.v3 
              WHERE LOWER(ticker) LIKE LOWER('%VCB%')
              ORDER BY dtyyyymmdd DESC
              LIMIT 10'''
              
    df = pd.read_sql(query, conn)
    
    ad = ((2 * df['close'].iloc[0]) - df['close'].iloc[1]) / (df['close'].iloc[0] + df['close'].iloc[1]) * df['close'].iloc[0]
    
    return [ad]
    
  except:
    return ["no query result"]
  
