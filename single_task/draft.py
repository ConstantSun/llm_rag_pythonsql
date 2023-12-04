import bedrock
import single_task.formula as formula
import single_task.dbtable_info as dbtable_info
import random
from datetime import datetime
import single_task.convert_db as convert_db
import streamlit
import os
import importlib


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
    print(".......ASK PYTHON CODE: ", question)
    print(type(question))
    start_time = datetime.now()
    formula_note = formula.ema + "\n\n" + formula.sma + "\n\n" + formula.rsi_2
    db_info = dbtable_info.dataupcom

    prompt_template_for_python_postgre = f"""You are both SQL expert and Python expert, and you work as both a Data Analysis and a Developer for a Securities Company (An Binh Securities Company)
Given an input question, create a syntactically correct python program, this program must use SQL query to run in Postgresql database using psycopg2 and pandas.read_sql.

<Highlight> 
If the question does not require to query the PostgreSQL database, do not make up answer, answer with this format: 
<answer>
<code>
```python 
def get_result():
    return "Không thể trả lời câu hỏi do không có thông tin từ cơ sở dữ liệu" 
```
</code>
</answer>
</Highlight>

Unless the user specifies in the question a specific number of examples to obtain, query for at most 10 results using the LIMIT clause as per SQL. You can order the results to return the most informative data in the database.

<note> When comparing ticker in SQL, use LIKE, LOWER() for both operands, do not use "=", e.g: To check if ticker equals to "Xyz", use: LOWER(ticker) LIKE LOWER('%Xyz%'). </note>

Only use the following formulas if the question mentions any of them, do not use your knowledge to create any formula if it is not mentioned below:

{formula_note}

<highlight> Pay attention to use only the column names you can see in the tables below. 
Be careful to not query for columns that do not exist. </highlight>
Only use the following database with tables: 

{db_info}

Return program's result in a function named get_result, the get_result function will return a string that answer the question with corresponding values.
Do not use print() function, python code format:  
<answer>
<code>
```python
<handle error> handle exception by returning "no query result" when SQL query does not return any value.</handle error> 
```
</code>
</answer>

If the Question wants to know any values, carefully check those formulas above, use "not found formula" to answer instead of using your own formula to answer the Question.
<question>
{question}
</question>"""
    ################################

    print("prompt_template_for_python_postgre: \n", prompt_template_for_python_postgre)
    
    def get_genereted_python_postgresql_code():
        return bedrock.ask_direct(prompt_template_for_python_postgre)

    genereted_python_code_postgresql = get_genereted_python_postgresql_code()

    print(f"\n_____@TIME EXECUTED_____SQL Postgres_______: {datetime.now()- start_time}\n\n{genereted_python_code_postgresql}" )
    
    
    #####################
    generated_python_athena_code = convert_db.postgres_to_athena(genereted_python_code_postgresql)
    generated_python_athena_code = strim_code(generated_python_athena_code)

    print(f"_____@TIME EXECUTED_____Athena SQL_______: {datetime.now()- start_time}\n\n{generated_python_athena_code}\n")
    print("----end-----------------\n", )


    file_name = "auto_gen_code"
    path = f'single_task/auto_gen/{file_name}.py'
    # Generate a separate Python file 
    with open(path, 'w') as f:
        f.write(generated_python_athena_code)

    # Import the function from the generated file
    spec = importlib.util.spec_from_file_location(file_name, os.path.join(os.getcwd(), path))

    generated_module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(generated_module)
    try:
        final_code_result = generated_module.get_result()
    except:
        final_code_result = "no query result"

    flag = False
    black_list_1 = ["xin chào", "không tìm", "không thể"]
    for word in black_list_1:
        if word in final_code_result[:10].lower():
            flag = True
    black_list_2 = [ "no query result" ,  "không có câu hỏi",  "không có kết quả",  "không có thông tin"]
    for word in black_list_2:
        if word in final_code_result[:20].lower():
            flag = True

    if flag:
        final_code_result = "_end_"
    else:
        streamlit.text(final_code_result)
        streamlit.text("_end_")        


    # if  not in black_list and "no query result" not in final_code_result and "không có câu hỏi" not in final_code_result[:20].lower() and "không có kết quả" not in final_code_result[:20].lower() and "không có thông tin" not in final_code_result[:20].lower():
    #     streamlit.text(final_code_result)
    #     streamlit.text("_end_")
        
    # else:
    #     # streamlit.text("_end_")
    #     final_code_result = "_end_"
    return final_code_result