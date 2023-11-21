import pyathena
import pandas as pd

def get_result():
    try:
        conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
        cursor = conn.cursor()
        
        # Get ticker info
        cursor.execute("SELECT ticker, name FROM company_info WHERE LOWER(ticker) LIKE LOWER('%ABB%')")
        ticker_info = cursor.fetchall()
        
        # Get stock data
        cursor.execute("""
            SELECT * FROM absdb.v3 
            WHERE LOWER(ticker) LIKE LOWER('%ABB%') 
            AND dtyyyymmdd BETWEEN '20220101' AND '20221231'
            ORDER BY dtyyyymmdd
            LIMIT 10
        """)
        stock_data = cursor.fetchall()
        
        df = pd.DataFrame(stock_data, columns=["ticker", "dtyyyymmdd", "open", "high", "low", "close", "volume"])
        
        result = [ticker_info, df.to_dict('records')]
        
        conn.close()
        return result
    
    except:
        return ["no query result"]
        
