# from draft import asynctest, multithread
# from single_task import multi_process, rag_flow, code_flow
# import time
# import asyncio
# from datetime import datetime
# import question_type
# from single_task import code_flow
# import bedrock

# t1 = datetime.now()
# asyncio.run(asynctest.main())
# t2 = time.time()
# print(f'Total time: {t2 - t1:.2f} secs')

# multithread.main()

# user_question = "Tôi muốn biết thông tin về mã chứng khoán ABB của Ngân hàng thương mại cổ phần An Bình trong năm 2022?"
# start_time = datetime.now()
# user_qstn_type = question_type.get_question_type(user_question)
# print("_____@TIME EXECUTED_____user_qstn_type: ", datetime.now() - start_time)

# res1, res2 = multi_process.get_answer(["Trong năm 2022, Ngân hàng An Bình đạt được những giải thưởng gì ?", 
#                                        "Chỉ xét trong năm 2022, không xét các năm khác, Ngân hàng An Bình có các sự kiện quan trọng nào?"])


# Mã ABB có chỉ số RSI là bao nhiêu?
# stock_code = "ABB"
# question = f"Mã {stock_code} có mức giá đóng cửa trung bình trong năm 2022 cao hơn bao nhiêu phần trăm so với mức giá đóng cửa trung bình trong năm 2021 ?"
# question =  "Mã ABB có chỉ số EMA cho 14 ngày là bao nhiêu?"

# percentage = code_flow.ask_python_code(question, t1)
# print("percentage: ", percentage)

# from single_task import multi_thread
# start = time.time()

# list = [[rag_flow.ask_rag, "Mã ABB có chỉ số EMA cho 14 ngày là bao nhiêu?"], [code_flow.ask_python_code, "Mã ABB có chỉ số EMA cho 14 ngày là bao nhiêu?"]]
# res = multi_thread.run_multi_funcs(list)
# print("--__--")
# print(res)
# print(f'Total time: {time.time() - start:.2f} secs')

# from draft import draft 
# draft.run()


# import importlib

# module_path = "single_task.auto_gen.auto_generated_python_athena_code"
# module = importlib.import_module(module_path)

# get_result = module.get_result
# print(get_result())

from single_task import multi_thread
import time

def func1(a, b, c):
    print("start ...................")
    t1 = time.time()
    ans1 = bedrock.ask_direct("tell me about Vietnam, less than 5 sentences.")
    print(f'{a} {b} {c} Total time - Vietnam: {time.time() - t1:.2f} secs')
    return [ans1]


def func2(x, y): 
    print("start ...................")
    t1 = time.time()
    ans1 = bedrock.ask_direct("tell me about you, less than 5 sentences.")
    print(f'{x} {y} Total time - Anthropic: {time.time() - t1:.2f} secs')
    return [ans1]


def func3(p, q, r):
    print("start ...................")
    t1 = time.time()
    ans1 = bedrock.ask_direct("tell me about Jeff Bezos, less than 5 sentences.")
    print(f'{p} {q} {r} Total time - Jeff bezos: {time.time() - t1:.2f} secs')
    return [ans1]

question_list = [
    [func1, (1,2,3)],
    [func2, (4,5) ],
    [func3, (10,11,12)]
]

# for q in question_list:
#     print(q[0])
#     print(q[1])
#     print("--------------------------------")

# res = multi_thread.run_multi_funcs(question_list)
# print(res)

from single_task import draft
print(draft.my_func())
