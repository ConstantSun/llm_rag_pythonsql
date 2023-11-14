import pandas as pd
from pyathena import connect

def get_result():
    # Connect to Athena
    conn = connect(aws_access_key_id=None, 
                   aws_secret_access_key=None,
                   s3_staging_dir='s3://abst-test-athena-log/',
                   region_name='us-east-1')
    
    cursor = conn.cursor()

    # Query to get the closing prices for VCB
    query = """
    SELECT dtyyyymmdd, close
    FROM absdb.v2 
    WHERE ticker = 'VCB'
    ORDER BY dtyyyymmdd
    """

    # Load data into Pandas DataFrame
    df = pd.read_sql(query, conn)

    # Calculate EMA  
    n = 14 # Number of periods for EMA
    df['EMA'] = df['close'].ewm(span=n, adjust=False).mean()

    # Return EMA values
    return df['EMA'].tolist()

print(get_result())
