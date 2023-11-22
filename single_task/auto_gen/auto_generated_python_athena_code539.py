import pyathena
import pandas as pd

def get_result():
    try:
        conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
        cursor = conn.cursor()
        
        # Get average closing price in 2021
        query = """SELECT AVG(close) as avg_close_2021 FROM absdb.v3 
                  WHERE LOWER(ticker) LIKE LOWER('%ABB%') AND 
                  EXTRACT(YEAR FROM dtyyyymmdd) = 2021"""
                  
        df_2021 = pd.read_sql(query, conn)
        
        # Get average closing price in 2022
        query = """SELECT AVG(close) as avg_close_2022 FROM absdb.v3 
                  WHERE LOWER(ticker) LIKE LOWER('%ABB%') AND 
                  EXTRACT(YEAR FROM dtyyyymmdd) = 2022"""
        
        df_2022 = pd.read_sql(query, conn)
        
        # Calculate percentage increase
        avg_close_2021 = df_2021['avg_close_2021'].values[0]
        avg_close_2022 = df_2022['avg_close_2022'].values[0]
        increase_pct = (avg_close_2022 - avg_close_2021) / avg_close_2021 * 100
        
        return [increase_pct]
    
    except:
        return ["no query result"]
        
