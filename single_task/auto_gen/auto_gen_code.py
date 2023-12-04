import pyathena
import pandas as pd

def get_result():
  try:
    conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
    cursor = conn.cursor()
    
    query = '''SELECT close FROM absdb.v3 WHERE LOWER(ticker) LIKE LOWER('%DVN%') ORDER BY dtyyyymmdd DESC LIMIT 15'''
    
    df = pd.read_sql(query, conn)
    closes = df['close'].tolist()
    closes.reverse()
    
    ups = 0
    downs = 0
    
    for i in range(len(closes)-1):
      change = closes[i] - closes[i+1]
      if change > 0:
        ups += change
      else:
        downs -= change
        
    if downs == 0:
      return "Không tìm thấy công thức tính RSI"
    
    rsi = 100 - (100 / (1 + ups / downs))
    
    return str(round(rsi, 2))
    
  except:
    return "Không có kết quả truy vấn"
  
