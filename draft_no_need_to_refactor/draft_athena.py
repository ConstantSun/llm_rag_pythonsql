
import pyathena
import pandas as pd

def get_result():
  conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
  cursor = conn.cursor()
  
  query = """
  SELECT dtyyyymmdd, close 
  FROM absdb.v2 
  WHERE ticker = 'ABB'
  ORDER BY dtyyyymmdd DESC
  LIMIT 14
  """
  
  df = pd.read_sql(query, conn)
  
  df = df.sort_values(by='dtyyyymmdd')
  
  closes = df['close'].tolist()
  closes.reverse() # reverse to calculate EMA from oldest to newest 
  
  ema_yesterday = closes[0] # first EMA is same as first closing price
  result = []
  
  for i in range(1, len(closes)):
    ema_today = (closes[i] - ema_yesterday) * (2 / (1 + 14)) + ema_yesterday
    result.append(ema_today)
    ema_yesterday = ema_today
    
  print("EMA indicator for VCB:", result)
  return result
  
get_result()