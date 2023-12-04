import pyathena
import pandas as pd

conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
cursor = conn.cursor()

def get_result():
  try:
    query = """SELECT close FROM absdb.v3 WHERE LOWER(ticker) LIKE LOWER('%DVN%') ORDER BY dtyyyymmdd DESC LIMIT 15"""
    df = pd.read_sql(query, conn)
    
    closes = df['close'].tolist()
    closes.reverse()
    
    ups = []
    downs = []
    
    for i in range(len(closes)-1):
      change = closes[i] - closes[i+1]
      if change > 0:
        ups.append(change)
      else:
        downs.append(abs(change))
        
    if len(ups) == 0 or len(downs) == 0:
      return 'Không tính được RSI do không có đủ dữ liệu'
    
    x = sum(ups)/14
    y = sum(downs)/14
    
    rsi = 100 - 100/(1 + x/y)
    
    return f'RSI của {len(closes)} ngày gần nhất của mã DVN là: {round(rsi, 2)}'
    
  except:
    return "Không có kết quả truy vấn"
