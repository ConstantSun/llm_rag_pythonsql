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
      LIMIT 15
    """)
    closes = cursor.fetchall()
    closes = [x[0] for x in closes]

    variations = []
    for i in range(len(closes)-1):
      variations.append(closes[i] - closes[i+1])
    
    positive_variations = [x for x in variations if x > 0]
    negative_variations = [abs(x) for x in variations if x < 0]

    x = sum(positive_variations) / 14
    y = sum(negative_variations) / 14

    rsi = 100 - (100 / (1 + x/y))

    return [round(rsi, 2)]

  except:
    return ["no query result"]
