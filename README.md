# RaQL Chatbot

RaQL Chatbot: Not only retrieve and extract your Knowledge document based on RAG, but also analyze complex data with auto-generated-progamming-code, gain insight into your Database to answer your question ! 

## App Logic Flow:
<img width="1414" alt="image" src="https://github.com/ConstantSun/llm_rag_pythonsql/assets/26327367/ad16d7c9-4f87-41f0-a422-d82be94d1efb">

## How to run:
#### Prepare env as the same as in https://github.com/ConstantSun/LLM_VNese_RAG , including set up Amz Opensearch, SageMaker endpoint

#### Then run:
```
$ pip install -r requirements.txt
$ python3 qna.py
```

#### Prepare Amazon Athena Database as following:
##### 1. Upload your csv file to S3 bucket, suppose your bucket is s3://project1/data/
##### 2. Go to AWS Glue -> Crawlers -> **Create crawler** : 
<img width="1403" alt="image" src="https://github.com/ConstantSun/llm_rag_pythonsql/assets/26327367/faa136c7-8dbc-4b8a-8af6-db83f66bd9a4">


##### 3. Fill out information step by step: 
<img width="1440" alt="image" src="https://github.com/ConstantSun/llm_rag_pythonsql/assets/26327367/7448dfcf-a955-48e7-9909-414acb260136">

#####  4. Click Next -> **Add a data source**
<img width="1151" alt="image" src="https://github.com/ConstantSun/llm_rag_pythonsql/assets/26327367/2b5622ff-f8e0-404c-8412-29559a51db00">

##### 5. In this config, remain default config except S3 path, insert your own s3://project1/data/ path in step 1. 

<img width="485" alt="image" src="https://github.com/ConstantSun/llm_rag_pythonsql/assets/26327367/3df91482-f34d-40b1-a432-bdf35e679d87">

-> Click **Add a S3 data source** -> Click **Next**

##### 6. Click Create new IAM Role:  
<img width="1195" alt="image" src="https://github.com/ConstantSun/llm_rag_pythonsql/assets/26327367/4ac21614-c07e-4370-ad25-eb03559e553e">
<img width="787" alt="image" src="https://github.com/ConstantSun/llm_rag_pythonsql/assets/26327367/6f34782b-e5f5-4858-9be7-a21acaff2ef1">

Click **Create**


Wait a second, you'll see IAM Role updated: 
<img width="1202" alt="image" src="https://github.com/ConstantSun/llm_rag_pythonsql/assets/26327367/9eabbbf0-bad2-46b7-b8df-7889f6e1e498">
-> Click Next

##### 7. Click **Add database**:
   <img width="1197" alt="image" src="https://github.com/ConstantSun/llm_rag_pythonsql/assets/26327367/7f94e939-fe3e-4deb-b6f5-662a2129850a">


Type your database name and click **Create database** :
<img width="1195" alt="image" src="https://github.com/ConstantSun/llm_rag_pythonsql/assets/26327367/0094c31e-8af9-4455-b095-09ceaacc9083">

#####  8. Select your newly created database and click Next: 
<img width="1205" alt="image" src="https://github.com/ConstantSun/llm_rag_pythonsql/assets/26327367/811dc1a1-d58e-4098-9452-2dd524fc58bd">

##### 9. Click **Create Crawler** :
<img width="1194" alt="image" src="https://github.com/ConstantSun/llm_rag_pythonsql/assets/26327367/cb5b3e5b-504c-416d-afd5-30699d229594">

##### 10. Click Run Crawler:
<img width="1190" alt="image" src="https://github.com/ConstantSun/llm_rag_pythonsql/assets/26327367/3564c839-d151-467d-b00a-1cd09a871347">

You'll see Crawler runs (1), wait a minute to finish crawl process.

##### 11. Go to Athena and select your database:
<img width="1390" alt="image" src="https://github.com/ConstantSun/llm_rag_pythonsql/assets/26327367/2409dd95-4c3e-4d92-8b26-85d1f7c5f167">

Check out **Tables and views** : 

<img width="398" alt="image" src="https://github.com/ConstantSun/llm_rag_pythonsql/assets/26327367/3444f592-c089-43a3-bb0b-0ff0d4227ab8">

##### 12. Due to wrong dtyyyymmdd Type, we'll run a query to create new table with correct format as below:
   
<img width="713" alt="image" src="https://github.com/ConstantSun/llm_rag_pythonsql/assets/26327367/3d033825-0119-4e06-98af-88008c377494">

Code: 
```
CREATE TABLE <your new table name> AS
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
FROM <your original table name>;
```
Click Run
