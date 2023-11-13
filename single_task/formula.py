ema = """This is EMA formula for today (EMA_today), to calculate EMA_today value, you need to calculate EMA yesterday value (EMA_yesterday) :
EMA_today = (stock closing price in today - EMA_yesterday) * (2 / (1 + Days)) + EMA_yesterday
Where :
EMA_today: EMA value today,
EMA_yesterday: EMA value yesterday,
Days: The total number of days.
Note: EMA_today value of the first day equals to Stock closing price today."""
sma = """
"""

rsi_vi = """When the question mentions RSI, it means Relative Strength Index in Securities. RSI của mã chứng khoán dao động từ 0 đến 100. Công thức:
- Tính biến đổi giữa giá đóng cửa của hai ngày liên tiếp.
- Lấy trung bình của lượng thay đổi tăng và thay đổi giảm trong 14 ngày.
- RSI = 100 - (100 / (1 + (Trung bình lượng thay đổi tăng / Trung bình lượng thay đổi giảm)))"""

rsi = """When the question mentions RSI, it means Relative Strength Index in Securities. RSI is a value in a range from 0 to 100. This is the formula:
Firstly, calculate the variation between the closing prices of two consecutive days.
Secondly, take the average of the amount of increase and decrease in 14 days. 
Finally, RSI = 100 - (100 / (1 + (Average amount of increase / Average amount of decrease)))"""