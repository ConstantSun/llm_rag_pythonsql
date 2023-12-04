import pyathena
import pandas as pd

conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
cursor = conn.cursor()

def get_result():
  try:
    query = """SELECT close FROM absdb.v3 WHERE LOWER(ticker) LIKE LOWER('%%NAB%%') ORDER BY dtyyyymmdd DESC LIMIT 14"""
    df = pd.read_sql(query, conn)
    close_prices = df['close'].tolist()
    sma = sum(close_prices) / len(close_prices)
    return str(round(sma, 2))
  
  except:
    return "Không tìm thấy kết quả"

