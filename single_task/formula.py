ema = """This is EMA formula: 
To calculate EMA value for N days, suppose day N is the most recent day and day 1 is the furtheast day, you need to calculate (N-1) EMA values 
Firstly, you need to calculate EMA value of <highlight> the furtheast (Day 1) </highlight>, 
Sencondly, you need to calculate EMA value of <highlight> the sencond furtheast (Day 2) </highlight>, 
etc, EMA value of Day N (this EMA value of Day N is the target and the result).

For each EMA value of Day i, excep Day 1 has EMA value equals to Closing Price, other Day i has EMA value equals to: EMA_today = (stock closing price in today - EMA_yesterday) * (2 / (1 + constant N)) + EMA_yesterday
Where :
EMA_today: EMA value today,
EMA_yesterday: EMA value yesterday,
N: a constant equals to the total number of days.
"""

sma = """This is SMA (Simple Moving Average) formula:
- Get the most recent 14 closing price values into an array.
- SMA equals to Mean of above array values."""

rsi_2 = """When the question mentions RSI, it means Relative Strength Index in Securities. RSI is a value in a range from 0 to 100. This is the formula:
- Retrieve 15 values of the most recent closing price by SQL query
- Reverse above array values
- Calculate 14 variation between closing prices of two consecutive elements in above array: array[i] - array[i-1]
- Calculate the value X equals to (sum of positive variation).
- Calculate the value Y equals to abs of (sum of negative variation).
- Calculate value: RSI = 100 - (100 / (1 + X / Y) )"""
