import pyathena
import pandas as pd

def get_result():
  try:
    conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
    cursor = conn.cursor()
    
    # Get 14 most recent closing prices 
    query = """SELECT close FROM absdb.v3 WHERE LOWER(ticker) LIKE LOWER('%VCB%') ORDER BY dtyyyymmdd DESC LIMIT 14"""
    df = pd.read_sql(query, conn)
    close_prices = df['close'].tolist()
    
    # Calculate AD
    ad = 0
    for i in range(len(close_prices)-1):
      ad += abs(close_prices[i] - close_prices[i+1])
      
    return [ad]
    
  except:
    return ["no query result"]
  
