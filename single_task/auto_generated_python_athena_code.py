import pyathena
import pandas as pd

def get_result():
  try:
    conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
    cursor = conn.cursor()
    
    # query = """SELECT high, low, close 
    #           FROM absdb.v2 
    #           WHERE LOWER(ticker) LIKE LOWER('%VCB%')
    #           ORDER BY dtyyyymmdd DESC
    #           LIMIT 10"""
    
    query = """WITH prices AS (
      SELECT ticker, dtyyyymmdd, close
      FROM absdb.v2
      WHERE LOWER(ticker) LIKE LOWER('%CV%')
      ORDER BY dtyyyymmdd DESC
      LIMIT 14
    ),
    gains AS (
      SELECT ticker, dtyyyymmdd, close - LAG(close) OVER (ORDER BY dtyyyymmdd) AS gain
      FROM prices
    ), 
    losses AS (
      SELECT ticker, dtyyyymmdd, LAG(close) OVER (ORDER BY dtyyyymmdd) - close AS loss
      FROM prices 
    ),
    avg_gains AS (
      SELECT AVG(gain) avg_gain
      FROM gains
    ),
    avg_losses AS (
      SELECT AVG(loss) avg_loss
      FROM losses
    )
    SELECT 100 - (100 / (1 + (avg_gain / avg_loss))) AS rsi
    FROM avg_gains, avg_losses
    LIMIT 1;"""
              
    df = pd.read_sql(query, conn)
    print("___df:")
    print(df)
    
    ad = ((df['high'] - df['low']) / (df['high'] + df['low'])) * df['close']
    
    return ad.tolist()
    
  except:
    return ["no query result"]
  
