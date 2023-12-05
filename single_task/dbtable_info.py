import env
dataupcom_db_name = env.dataupcom_db_name # TODO: change this to your own database name, note : DO NOT USE characters other than a-z, A-Z, 0-9.
table_name = env.table_name  # TODO: change this to your own table name, note : DO NOT USE characters other than a-z, A-Z, 0-9.
dataupcom = f"""Database name: {dataupcom_db_name}
Table name: {table_name}
<table>
Columns:
"ticker": string, description: Ticker symbol or Stock symbol
"dtyyyymmdd": date type, description: date type
"open": double, description: stock opening price
"high": double, description: stock highest price
"low": double, description: stock lowest price
"close": double, description: stock closing price
"volume": bigint, description: trading volume
Note: dtyyyymmdd has Date type, if compare dtyyyymmdd BETWEEN varchar() and varchar(), remember to add date before varchar() time string,
e.g: WHERE dtyyyymmdd BETWEEN date '2021-01-01' AND date '2021-01-31' 
</table>"""
