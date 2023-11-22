import pyathena
import pandas as pd

conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
cursor = conn.cursor()

def get_result():
  try:
    cursor.execute("""
      SELECT close
      FROM absdb.v3
      WHERE LOWER(ticker) LIKE LOWER('%ABB%')
      ORDER BY dtyyyymmdd DESC
      LIMIT 14
    """)
    closes = cursor.fetchall()
    closes = [x[0] for x in closes]
    sma = sum(closes) / len(closes)
    return [sma]
  except:
    return ["no query result"]
