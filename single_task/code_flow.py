import bedrock
import single_task.formula as formula
import single_task.dbtable_info as dbtable_info
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
    Given an input question, create a syntactically correct python program, this program might use PostgreSQL's query to run, the result is the return value of get_result() function

    {formula_note}

    Only use the following database with tables:
    {db_info}

    Question: {question}, you only answer the python code
    """
    ################################

    print("prompt_template_for_python_postgre: \n", prompt_template_for_python_postgre)
    def get_genereted_python_postgresql_code():
        return bedrock.llm(prompt_template_for_python_postgre)

    genereted_python_code_postgresql = get_genereted_python_postgresql_code()

    ################################
    prompt_template_for_python_athena = f"""Convert the following python code so that it connects to Amazon Athena database instead of PostgreSQL, using PyAthena library, aws_access_key_id is None and aws_secret_access_key is None  :
    {genereted_python_code_postgresql}
    """
    def get_generated_python_athena_code():
        return bedrock.llm(prompt_template_for_python_athena)
    
    generated_python_athena_code = get_generated_python_athena_code()

    # write that code above to a .py file
    text_file = open("generated_python_athena_code.py", "w")
    text_file.write(generated_python_athena_code)

    # import that file and get the result
    import generated_python_athena_code
    final_code_result = get_generated_python_athena_code.get_result()

    return final_code_result