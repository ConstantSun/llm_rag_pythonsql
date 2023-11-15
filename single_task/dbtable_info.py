dataupcom_db_name = "absdb"
dataupcom = f"""Database name: {dataupcom_db_name}
Table name: v2
Columns:
"ticker": string, description: Ticker symbol or Stock symbol
"dtyyyymmdd": bigint, description: date time, format : year-month-day
"open": double, description: stock opening price
"high": double, description: stock highest price
"low": double, description: stock lowest price
"close": double, description: stock closing price
"volume": bigint, description: trading volume
Note: Colum "dtyyyymmdd" is bigint, therefore instead of EXTRACT time from dtyyyymmdd, compare it to a range, e.g: to check if dtyyyymmdd is within May, 2023, check if dtyyyymmdd is less or equal to 20230531 and dtyyyymmdd is greater or equal to 20230501"""

