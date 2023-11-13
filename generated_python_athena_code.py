 Here is how to modify the code to use PyAthena to connect to Athena instead of PostgreSQL:

```python
import pandas as pd
from pyathena import connect

conn = connect(aws_access_key_id=None, aws_secret_access_key=None, s3_staging_dir='s3://my-athena-results/', region_name='us-west-2')

cursor = conn.cursor()

cursor.execute("""
    SELECT dtyyyymmdd, close
    FROM stock_prices 
    WHERE ticker = 'ABB'
    ORDER BY dtyyyymmdd DESC 
    LIMIT 14
""")

df = cursor.fetchall()

ema_yesterday = df[0][1] 

for i in range(1,14):
    close = df.iloc[i][1]
    ema_today = (close - ema_yesterday) * (2 / (14 + 1)) + ema_yesterday
    ema_yesterday = ema_today

print(ema_today)

conn.close()
```

The main changes are:

- Import PyAthena and connect to Athena with the connect() function instead of psycopg2 and PostgreSQL  
- Specify the Athena workgroup location with s3_staging_dir
- Use a cursor to execute the query on the Athena table instead of PostgreSQL
- Fetch results into a Pandas DataFrame instead of a list
- Access the close prices by index on the DataFrame instead of the list

The EMA calculation remains the same otherwise. This allows querying an Athena database similarly to PostgreSQL.