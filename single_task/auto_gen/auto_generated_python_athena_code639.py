import pyathena
import pandas as pd

conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
cursor = conn.cursor()

def get_result():
  try:
    query = """SELECT * FROM absdb.v3 WHERE LOWER(ticker) LIKE LOWER('%ABB%') ORDER BY dtyyyymmdd DESC LIMIT 15"""
    df = pd.read_sql(query, conn)
    
    closes = df['close'].to_list()
    variations = []
    for i in range(len(closes)-1):
      variations.append(closes[i+1] - closes[i])
    
    X = sum([x for x in variations if x > 0]) / 14
    Y = sum([abs(x) for x in variations if x < 0]) / 14
    
    rsi = 100 - (100 / (1 + X/Y))
    
    return [round(rsi, 2)]
    
  except:
    return ["no query result"]
  
