import pyathena
import pandas as pd

def get_result():
    try:
        conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
        cursor = conn.cursor()
        
        query = '''SELECT * FROM absdb.v3 
                   WHERE LOWER(ticker) LIKE LOWER('%JKL%') 
                   AND dtyyyymmdd BETWEEN '2022-10-01' AND '2022-10-31'
                   ORDER BY dtyyyymmdd DESC
                   LIMIT 10'''
                   
        df = pd.read_sql(query, conn)
        
        return df['close'].tolist()
        
    except:
        return ["no query result"]
        
