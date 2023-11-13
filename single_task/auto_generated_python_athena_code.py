import pandas as pd
from pyathena import connect

def get_result():
    conn = connect(aws_access_key_id=None, 
                   aws_secret_access_key=None,
                   s3_staging_dir='s3://abst-test-athena-log/',
                   region_name='us-east-1')
    
    cursor = conn.cursor()

    query = """
    SELECT ticker, dtyyyymmdd, close
    FROM absdb.v2 
    WHERE ticker = 'ABB' 
    ORDER BY dtyyyymmdd DESC 
    LIMIT 14
    """

    df = pd.read_sql(query, conn)
    
    sma = df['close'].rolling(window=14).mean().iloc[-1]
    
    return [sma]

result = get_result()
print(result)
