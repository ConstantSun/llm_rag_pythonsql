# import os
# import importlib

# # Relative path
# module_path = 'single_task.auto_gen.auto_generated_python_athena_code597'

# # Get absolute path
# absolute_path = os.path.abspath(module_path)
# print("abs path: ", absolute_path)
# absolute_path = absolute_path.replace("/", ".")
# # Import module directly using absolute path
# result = importlib.import_module(absolute_path[1:])


# # Use module
# res = result.get_result()


import importlib
import single_task
import os

def test():
    # Absolute path to the module
    p = 'single_task.auto_gen.auto_generated_python_athena_code597' 


    module = importlib.import_module(p)  

    # Use module
    res = module.get_result()
    return res