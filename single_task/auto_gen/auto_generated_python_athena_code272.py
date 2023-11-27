import pyathena
import pandas as pd

def get_result():
    try:
        conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
        cursor = conn.cursor()
        
        # Lấy giá đóng cửa trung bình năm 2021
        query = """SELECT AVG(close) AS avg_close_2021 FROM absdb.v3 
                  WHERE LOWER(ticker) LIKE LOWER('%ABB%') AND dtyyyymmdd BETWEEN date '2021-01-01' AND date '2021-12-31'"""
        df_2021 = pd.read_sql(query, conn)
        
        # Lấy giá đóng cửa trung bình năm 2022
        query = """SELECT AVG(close) AS avg_close_2022 FROM absdb.v3 
                  WHERE LOWER(ticker) LIKE LOWER('%ABB%') AND dtyyyymmdd BETWEEN date '2022-01-01' AND date '2022-12-31'"""
        df_2022 = pd.read_sql(query, conn)
        
        # Tính phần trăm tăng giảm
        increase_percent = (df_2022.iloc[0,0] - df_2021.iloc[0,0]) / df_2021.iloc[0,0] * 100
        
        return [increase_percent]
    
    except:
        return ["no query result"]
        
