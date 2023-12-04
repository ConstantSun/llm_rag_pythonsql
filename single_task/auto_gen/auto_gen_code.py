import pyathena
import pandas as pd

def get_result():
    try:
        conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
        cursor = conn.cursor()
        
        query = '''SELECT * FROM absdb.v3 
                   WHERE LOWER(ticker) LIKE LOWER('%NAB%') 
                   AND dtyyyymmdd BETWEEN date '2021-09-01' AND date '2021-09-30'
                   LIMIT 10'''
                   
        df = pd.read_sql(query, conn)
        
        if df.empty:
            return "Không tìm thấy thông tin về mã NAB trong tháng 9"
        
        result = "Có " + str(len(df)) + " kết quả cho mã NAB trong tháng 9:"
        for index, row in df.iterrows():
            date = row['dtyyyymmdd'].strftime('%Y-%m-%d')
            result += "\nNgày " + date + \
                      "\nGiá mở cửa: " + str(row['open']) + \
                      "\nGiá cao nhất: " + str(row['high']) + \
                      "\nGiá thấp nhất: " + str(row['low']) + \
                      "\nGiá đóng cửa: " + str(row['close']) + \
                      "\nKhối lượng giao dịch: " + str(row['volume'])
                      
        return result
    
    except Exception as e:
        return "Không thể truy vấn cơ sở dữ liệu"
    
