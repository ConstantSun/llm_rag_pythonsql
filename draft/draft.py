def run():
  moduleNames = ['single_task.auto_gen.auto_generated_python_athena_code'] 
  modules = __import__(moduleNames[0])
  print(modules.get_result())