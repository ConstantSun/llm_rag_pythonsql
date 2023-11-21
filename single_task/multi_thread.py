# import time
from threading import Thread
from queue import Queue
# import bedrock

# def func1(quest):
#     print("start ...................")
#     t1 = time.time()
#     ans1 = bedrock.llm(quest)
#     print(f'Total time - Vietnam: {time.time() - t1:.2f} secs')

#     return [ans1]

# def func2(quest):
#     print("start ...................")
#     t1 = time.time()
#     ans2 = bedrock.llm(quest)
#     print(f'Total time - singapore: {time.time() - t1:.2f} secs')

#     return [ans2]

# nums = [1,2,3,4,5]

def wrapper(func, arg, queue):
    queue.put(func(arg))

def run_multi_funcs(list_of_pair_of_func_param: list[list]):
    """
    Run multiple functions in parallel.
    Params: 
    list_of_pair_of_func_param: list of list of function and its params, e.g: [[function, function_params: a str or a number]]
    Returns: list of function return values
    """
    q = []
    for i in range(len(list_of_pair_of_func_param)):
        q.append(Queue())
    for i in range(len(list_of_pair_of_func_param)):
        Thread(target=wrapper, args=(list_of_pair_of_func_param[i][0], list_of_pair_of_func_param[i][1], q[i])).start()
    return [qi.get() for qi in q]

