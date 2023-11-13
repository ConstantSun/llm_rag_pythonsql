import bedrock
import single_task.formula as formula
import single_task.dbtable_info as dbtable_info
import env


def strim_code(raw_answer: str):
    strim_ans = ""
    flag = False
    print("----Strim code-----------------\n", )
    for line in raw_answer.splitlines():
        print(line)
        if "```python" in line:
            print("START___________")
            flag = True
            continue

        elif "```" in line:
            print("END_______________")
            flag = False
        
        if flag:
            strim_ans += line + "\n"

    print("----end-----------------\n", )
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
    formula_note = formula.ema
    db_info = dbtable_info.dataupcom

    prompt_template_for_python_postgre = f"""You are an expert in Stock Market and you are also a SQL expert and Python expert, and you work as both a Data Analysis and a Developer for a Securities Company.
Given an input question, create a syntactically correct python program, this program might use PostgreSQL's query to run:

{formula_note}

Only use the following database with tables:
{db_info}

Question: "{question}", you only answer the python code
    """
    ################################

    print("prompt_template_for_python_postgre: \n", prompt_template_for_python_postgre)
    def get_genereted_python_postgresql_code():
        return bedrock.llm(prompt_template_for_python_postgre)

    genereted_python_code_postgresql = get_genereted_python_postgresql_code()

    print("----SQL Postgres---------------\n", genereted_python_code_postgresql)
    
    
    ################################
    prompt_template_for_python_athena = f"""Convert the following python code, so that it connects to Amazon Athena database instead of PostgreSQL, using PyAthena library, the database name and table names are all the same in PostgreSQL, aws_access_key_id is {env.aws_access_key_id}, aws_secret_access_key is {env.aws_secret_access_key}, s3 bucket is {env.athena_s3_bucket}, region_name is {env.region_name} :
    {genereted_python_code_postgresql}
    """
    def get_generated_python_athena_code():
        return bedrock.llm(prompt_template_for_python_athena)
    
    generated_python_athena_code = get_generated_python_athena_code()
    # generated_python_athena_code = strim_code(generated_python_athena_code)

    print("----Athena SQL-----------------\ngenerated_python_athena_code: \n", generated_python_athena_code)
    
    generated_python_athena_code = strim_code(generated_python_athena_code)

    
    print("----Strim Athena SQL-----------------\n", generated_python_athena_code)
    print("----end-----------------\n", )
    ################################
    # write that code above to a .py file
    text_file = open("single_task/generated_python_athena_code.py", "w")
    text_file.write(generated_python_athena_code)

    # # import that file and get the result
    # import generated_python_athena_code
    # final_code_result = get_generated_python_athena_code.get_result()

    return 