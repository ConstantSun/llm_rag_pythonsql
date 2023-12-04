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
- Retrieve 15 values of the most recent closing price, assuming day 15 is the most recent day, and day 1 is the farthest day.
- Calculate the variation between closing prices of two consecutive days, specifically calculate 14 values as follows: closing price on day n+1 minus closing price on day n, closing price on day n minus closing price on day n-1, .... until the closing price of day 2 minus the closing price of day 1.
- Calculate the value X, X equals to (sum of positive variation)/14.
- Calculate the value Y, Y equals to abs of (sum of negative variation)/14.
- Calculate value: RSI = 100 - (100 / (1 + X / Y) )"""

# rsi = """When the question mentions RSI, it means Relative Strength Index in Securities. RSI is a value in a range from 0 to 100. This is the formula:
# Firstly, calculate the variation between the closing prices of two consecutive days.
# Secondly, take the average of the amount of increase and decrease in 14 days. 
# Finally, RSI = 100 - (100 / (1 + (Average amount of increase / Average amount of decrease)))"""
