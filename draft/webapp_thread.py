import streamlit as st
from threading import Thread
from streamlit.runtime.scriptrunner import add_script_run_ctx
from queue import Queue
from single_task import rag_flow
from langchain.callbacks import StreamlitCallbackHandler

def wrapper(func, arg, queue):
    print("---------- wrapper arg: ", arg)
    queue.put(func(*arg))

def run_multi_funcs(list_of_pair_of_func_param: list[list]):
    """
    Run multiple functions in parallel.
    Params: 
    list_of_pair_of_func_param: list of list of function and its params, e.g: [[function, (function_params): a tuple of multi str or number]]
    
    Returns: 
    list of function return values
    """
    q = []
    for i in range(len(list_of_pair_of_func_param)):
        q.append(Queue())
    for i in range(len(list_of_pair_of_func_param)):
        print("run_multi_funcs, func # :", i)
        print(list_of_pair_of_func_param[i])
        t = Thread(target=wrapper, args=( list_of_pair_of_func_param[i][0], list_of_pair_of_func_param[i][1], q[i]  ) )
        add_script_run_ctx(t)
        t.start()
    return [qi.get() for qi in q]

def func1(text:str):
    st_callback = StreamlitCallbackHandler(st.container())

    rag_flow.ask_streaming_rag(streaming_callback=st_callback, query="công ty bạn có dịch vụ gì?")
    # st.text(text + "  1")

def func2(text:str):
    st_callback = StreamlitCallbackHandler(st.container())

    rag_flow.ask_streaming_rag(streaming_callback=st_callback, query="năm 2022, ngân hàng An Bình giành được giải thưởng gì?")

    # st.text(text + " 2")


run_multi_funcs([
    [func1, ("Hello 1",)],
    [func2, ("World 2",)]
])


st.text("Background")

# def target():
#     st.text_area("Thread !")
#     st.text("thread")

# t = Thread(target=target)
# add_script_run_ctx(t)
# t.start()
