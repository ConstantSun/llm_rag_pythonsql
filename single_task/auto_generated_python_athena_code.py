import pandas as pd
from pyathena import connect

def get_result():

  # Connect to Athena
  conn = connect(aws_access_key_id=None, 
                 aws_secret_access_key=None,
                 s3_staging_dir='s3://abst-test-athena-log/',
                 region_name='us-east-1')
  
  cursor = conn.cursor()

  # Query to get closing prices
  query = """SELECT close FROM abs-test-1.v2v2 WHERE ticker='ABB' ORDER BY dtyyyymmdd DESC LIMIT 14"""

  df = pd.read_sql(query, conn)
  
  closes = df['close'].tolist()

  # Calculate EMA
  ema_yesterday = closes[0]
  days = 14
  k = 2 / (days + 1)
  ema_today = (closes[0] - ema_yesterday) * k + ema_yesterday

  for close in closes[1:]:
    ema_yesterday = ema_today
    ema_today = (close - ema_yesterday) * k + ema_yesterday

  return [ema_today]

print(get_result())
