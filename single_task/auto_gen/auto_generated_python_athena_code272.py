import pyathena
import pandas as pd


def get_result():
    try:
        conn = pyathena.connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://abst-test-athena-log/', region_name='us-east-1')
        cursor = conn.cursor()
        
        # Get the most recent 14 closing prices for TOP stock
        query = """SELECT close 
                FROM absdb.v3
                WHERE LOWER(ticker) LIKE LOWER('%TOP%')
                ORDER BY dtyyyymmdd DESC
                LIMIT 14"""
                
        cursor.execute(query)
        prices = cursor.fetchall()
        closes = [price[0] for price in prices]
        
        # Calculate SMA
        sma = sum(closes) / len(closes)
        
        # Calculate RSI
        ups = [max(0, closes[i] - closes[i+1]) for i in range(len(closes)-1)] 
        downs = [max(0, closes[i+1] - closes[i]) for i in range(len(closes)-1)]
        avg_up = sum(ups)/14
        avg_down = sum(downs)/14
        rs = avg_up / avg_down
        rsi = 100 - (100/(1+rs))
        
        # Get latest close price
        query = """SELECT close
                FROM absdb.v3
                WHERE LOWER(ticker) LIKE LOWER('%TOP%')
                ORDER BY dtyyyymmdd DESC
                LIMIT 1"""
                
        cursor.execute(query)
        latest_close = cursor.fetchone()[0]
        
        conn.close()
        
        return f"SMA: {sma:.2f}, RSI: {rsi:.2f}, Latest close price: {latest_close:.2f}"
    
    except:
        return "no query result"
    
        
print(get_result())    
    
