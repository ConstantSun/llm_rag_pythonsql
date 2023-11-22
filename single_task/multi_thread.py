from threading import Thread
from queue import Queue

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

