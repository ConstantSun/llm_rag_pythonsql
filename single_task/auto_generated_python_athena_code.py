import pyathena
import pandas as pd

def get_result():
  try:
    conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
    cursor = conn.cursor()
    
    # Calculate RSI
    query = """
    SELECT ticker, dtyyyymmdd, close 
    FROM absdb.v3
    WHERE LOWER(ticker) LIKE LOWER('%ABB%')
    ORDER BY dtyyyymmdd DESC
    LIMIT 14"""
    
    df = pd.read_sql(query, conn)
    df = df.sort_values('dtyyyymmdd')
    
    delta = df['close'].diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    
    avg_gain = up.rolling(14).mean()
    avg_loss = down.abs().rolling(14).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    rsi_abb = round(rsi.iloc[-1], 2)
    
    return [rsi_abb]
    
  except:
    return ["no query result"]
  
