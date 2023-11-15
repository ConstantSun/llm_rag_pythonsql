import psycopg2

conn = psycopg2.connect(database="absdb", user='postgres', password='123', host='127.0.0.1', port= '5432')
cursor = conn.cursor()

def get_result():
  cursor.execute("""
  SELECT close 
  FROM v2 
  WHERE ticker = 'VCB'
  ORDER BY dtyyyymmdd DESC
  LIMIT 10
  """)

  closes = cursor.fetchall()
  closes.reverse()

  ema_yesterday = closes[0][0]

  days = len(closes)

  emas = [closes[0][0]]

  for close in closes[1:]:
    ema_today = (close[0] - ema_yesterday) * (2 / (1 + days)) + ema_yesterday
    emas.append(ema_today)
    ema_yesterday = ema_today

  return emas