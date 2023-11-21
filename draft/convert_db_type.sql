CREATE TABLE v3 AS
SELECT
  ticker,
  CAST(CONCAT(
       SUBSTR(CAST(dtyyyymmdd AS VARCHAR), 1, 4), '-',  
       SUBSTR(CAST(dtyyyymmdd AS VARCHAR), 5, 2), '-',
       SUBSTR(CAST(dtyyyymmdd AS VARCHAR), 7, 2)
  ) AS DATE) AS dtyyyymmdd,
  open,
  high,
  low,
  close,
  volume
FROM v2;