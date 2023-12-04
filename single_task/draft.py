# import importlib
# import single_task
# import os

# def test():
#     # Absolute path to the module
#     p = 'single_task.auto_gen.auto_generated_python_athena_code597' 


#     module = importlib.import_module(p)  

#     # Use module
#     res = module.get_result()
#     return res


import os
import importlib

path = 'single_task/auto_gen/generated_file.py'
# Generate a separate Python file 
with open(path, 'w') as f:
    f.write("""
def my_func():
    return 'Generated function called, hang 1!'
""")

# Import the function from the generated file
spec = importlib.util.spec_from_file_location("generated_file", os.path.join(os.getcwd(), path))

generated_module = importlib.util.module_from_spec(spec)

spec.loader.exec_module(generated_module)
my_func = generated_module.my_func

# Call the imported function and print result
