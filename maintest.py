# from draft import asynctest, multithread
from single_task import multi_process
import time
# import asyncio
from datetime import datetime
import question_type
from single_task import code_flow
import bedrock

t1 = datetime.now()
# asyncio.run(asynctest.main())
# t2 = time.time()
# print(f'Total time: {t2 - t1:.2f} secs')

# multithread.main()

# user_question = "Tôi muốn biết thông tin về mã chứng khoán ABB của Ngân hàng thương mại cổ phần An Bình trong năm 2022?"
# start_time = datetime.now()
# user_qstn_type = question_type.get_question_type(user_question)
# print("_____@TIME EXECUTED_____user_qstn_type: ", datetime.now() - start_time)

# res1, res2 = multi_process.get_answer(["Trong năm 2022, Ngân hàng An Bình đạt được những giải thưởng gì ?", 
#                                        "Chỉ xét trong năm 2022, không xét các năm khác, Ngân hàng An Bình có các sự kiện quan trọng nào?"])


# Mã ABB có chỉ số RSI là bao nhiêu?
stock_code = "ABB"
question = f"Mã {stock_code} có mức giá đóng cửa trung bình trong năm 2022 cao hơn bao nhiêu phần trăm so với mức giá đóng cửa trung bình trong năm 2021 ?"
question =  "Mã ABB có chỉ số RSI là bao nhiêu?"

percentage = code_flow.ask_python_code(question, t1)
print("percentage: ", percentage)

question = """You are an expert in Stock Market and you are also a SQL expert and Python expert, and you work as both a Data Analysis and a Developer for a Securities Company.
Given an input question, create a syntactically correct python program, this program might use SQL query to run in Postgresql database using psycopg2 and pandas.read_sql. Unless the user specifies in the question a specific number of examples to obtain, query for at most 10 results using the LIMIT clause as per SQL. You can order the results to return the most informative data in the database.
When searching in SQL, use LIKE, LOWER(), e.g: To check if ticker equals to "Xyz", then use: LOWER(ticker) LIKE LOWER('%Xyz%'), always LOWER() both objects and use LIKE.

Only use the following formulas if the question mentions any of them, do not use your knowledge to create any formula if it is not mentioned below:
This is EMA formula: 
To calculate EMA_today value, you need to calculate EMA yesterday value (EMA_yesterday), e.g: if you want to calculate EMA value for N days, you need to calculate EMA value of 1st day, EMA value of 2nd day, EMA value of 3rd day, etc, EMA value of N-th day (this EMA value of N-th day is the target and the result).
EMA_today = (stock closing price in today - EMA_yesterday) * (2 / (1 + constant N)) + EMA_yesterday
Where :
EMA_today: EMA value today,
EMA_yesterday: EMA value yesterday,
N: a constant equals to the total number of days.
Note: EMA_today value of the first day equals to Stock closing price today.


This is SMA (Simple Moving Average) formula:
SMA = Mean of Total Closing Price within 14 days.

When the question mentions RSI, it means Relative Strength Index in Securities. RSI is a value in a range from 0 to 100. This is the formula:
Firstly, calculate the variation between the closing prices of two consecutive days.
Secondly, take the average of the amount of increase and decrease in 14 days. 
Finally, RSI = 100 - (100 / (1 + (Average amount of increase / Average amount of decrease)))

Only use the following database with tables:
Database name: absdb
Table name: v3
Columns:
"ticker": string, description: Ticker symbol or Stock symbol
"dtyyyymmdd": date, description: date type
"open": double, description: stock opening price
"high": double, description: stock highest price
"low": double, description: stock lowest price
"close": double, description: stock closing price
"volume": bigint, description: trading volume

Return program's result in a function named get_result, the get_result function will return an array of target value(s), do not use print() function, start the python code with the line: 
```python
and end the python code with the line:
```
and handle exception by returning "no query result" when SQL query does not return any value.

If the Question wants to know any values, carefully check those formulas above, do not use your own formula to answer the Question and answer "not found formula" if you can not find the formula.
Question: "Mã ABB có chỉ số RSI là bao nhiêu?" """
# print(bedrock.ask_direct(question))