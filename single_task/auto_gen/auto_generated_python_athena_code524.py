import pyathena
import pandas as pd

def get_result():
  try:
    conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
    cursor = conn.cursor()
    
    query = '''SELECT close FROM absdb.v3 WHERE LOWER(ticker) LIKE LOWER('%%TOP%%') AND dtyyyymmdd BETWEEN date '2023-08-01' AND date '2023-08-31' ORDER BY dtyyyymmdd DESC LIMIT 1'''
    
    cursor.execute(query)
    result = cursor.fetchone()
    
    if result:
      return str(result[0])
    else:
      return "Không tìm thấy kết quả"
      
  except:
    return "Không thể truy vấn cơ sở dữ liệu"
  
print(get_result())
