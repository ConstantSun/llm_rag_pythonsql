import pyathena
import pandas as pd

def get_result():
  try:
    conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
    cursor = conn.cursor()
    
    query = '''SELECT * FROM absdb.v3 WHERE LOWER(ticker) LIKE LOWER('%ABB%') ORDER BY dtyyyymmdd DESC LIMIT 15'''
    
    df = pd.read_sql(query, conn)
    
    closes = df['close'].tolist()
    
    ups = []
    downs = []
    
    for i in range(len(closes)-1):
      diff = closes[i] - closes[i+1]
      if diff > 0:
        ups.append(diff)
      else:
        downs.append(abs(diff))
        
    x = sum(ups)/14
    y = sum(downs)/14
    
    rsi = 100 - (100/(1 + x/y))
    
    return [rsi]
    
  except:
    return ["no query result"]
  
