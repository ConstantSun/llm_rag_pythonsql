import bedrock
import single_task.formula as formula
import single_task.dbtable_info as dbtable_info
import random
from datetime import datetime
import single_task.convert_db as convert_db

def strim_code(raw_answer: str):
    strim_ans = ""
    flag = False
    for line in raw_answer.splitlines():
        if "```python" in line:
            flag = True
            continue
        elif "```" in line:
            flag = False
        
        if flag:
            strim_ans += line + "\n"
    return strim_ans


def ask_python_code(question: str):
    """
    Param: question : str
    Return: Result value
    
    Includes 3 steps:
    Step 1: Generate python code, might connect to SQL postgresql
    Step 2: Convert to python code, might connect to AMZ Athena
    Step 3: Execute step 2's code, return result
    """
    start_time = datetime.now()
    formula_note = formula.ema + "\n\n" + formula.sma + "\n\n" + formula.rsi_2
    db_info = dbtable_info.dataupcom

    prompt_template_for_python_postgre = f"""You are an expert in Stock Market and you are also a SQL expert and Python expert, and you work as both a Data Analysis and a Developer for a Securities Company.
Given an input question, create a syntactically correct python program, this program might use SQL query to run in Postgresql database using psycopg2 and pandas.read_sql. Unless the user specifies in the question a specific number of examples to obtain, query for at most 10 results using the LIMIT clause as per SQL. You can order the results to return the most informative data in the database.
When comparing ticker in SQL, use LIKE, LOWER() for both operands, do not use "=", e.g: To check if ticker equals to "Xyz", then use: LOWER(ticker) LIKE LOWER('%Xyz%').

Only use the following formulas if the question mentions any of them, do not use your knowledge to create any formula if it is not mentioned below:
{formula_note}

Only use the following database with tables:
{db_info}

Return program's result in a function named get_result, the get_result function will return an array of target value(s), do not use print() function, start the python code with the line: 
```python
and end the python code with the line:
```
and handle exception by returning "no query result" when SQL query does not return any value.

If the Question wants to know any values, carefully check those formulas above, do not use your own formula to answer the Question and answer "not found formula" if you can not find the formula.
Question: "{question}" """
    ################################

    print("prompt_template_for_python_postgre: \n", prompt_template_for_python_postgre)
    
    def get_genereted_python_postgresql_code():
        return bedrock.ask_direct(prompt_template_for_python_postgre)

    genereted_python_code_postgresql = get_genereted_python_postgresql_code()

    print(f"\n_____@TIME EXECUTED_____SQL Postgres_______: {datetime.now()- start_time}\n\n{genereted_python_code_postgresql}" )
    
    
    ################################
    # prompt_template_for_python_athena = f"""Convert the following python code, so that it connects to Amazon Athena database instead of PostgreSQL, using PyAthena library, Amazon Athena table name is the same as table's name in PostgreSQL, the Amazon Athena table has a prefix: "{dbtable_info.dataupcom_db_name}", aws_access_key_id is {env.aws_access_key_id}, aws_secret_access_key is {env.aws_secret_access_key}, s3 bucket is {env.athena_s3_bucket}, region_name is {env.region_name}, return program's result in a function named get_result, the get_result function will return an array of target value(s):
    # {genereted_python_code_postgresql}
    # """
    
    # def get_generated_python_athena_code():
    #     return bedrock.llm(prompt_template_for_python_athena)
    
    # generated_python_athena_code = get_generated_python_athena_code()
    # # generated_python_athena_code = strim_code(generated_python_athena_code)

    #####################
    generated_python_athena_code = convert_db.postgres_to_athena(genereted_python_code_postgresql)
    generated_python_athena_code = strim_code(generated_python_athena_code)

    print(f"_____@TIME EXECUTED_____Athena SQL_______: {datetime.now()- start_time}\n\n{generated_python_athena_code}\n")
    print("----end-----------------\n", )
    ################################
    # write that code above to a .py file
    # file_name = "auto_generated_python_athena_code" + str(random.randint(0, 1000))
    file_name = "auto_generated_python_athena_code" 
    text_file = open(f"single_task/{file_name}.py", "w")
    text_file.write(generated_python_athena_code)
    text_file.close()

    # import that file and get the result
    import single_task.auto_gen.auto_generated_python_athena_code as auto_generated_python_athena_code
    final_code_result = auto_generated_python_athena_code.get_result()

    return final_code_result


def test_ask_python_code(question: str):

    # import that file and get the result
    import llm_rag_pythonsql.single_task.auto_gen.auto_generated_python_athena_code as auto_generated_python_athena_code
    final_code_result = auto_generated_python_athena_code.get_result()

    return final_code_result
