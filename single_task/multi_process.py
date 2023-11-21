from multiprocessing import Pool
from single_task import rag_flow
import time

def f(question:str):
    print("start ...................")
    t1 = time.time()
    ans1 = rag_flow.ask_rag(question) 
    t2 = time.time()
    print(f'Total time: {t2 - t1:.2f} secs')
    print("end ...................")
    return ans1

def get_answer(question_list: list[str]) -> list[str]:
    """
    Param: question_list
    Return: list of corresponding answers by bedrock, run in parallel
    Note: question_list should not have more than 4 questions due to # of this computer's vCPU 
    """
    with Pool(6) as p:
        result = (p.map(f, 
        # ["Trong năm 2022, Ngân hàng An Bình đạt được những giải thưởng gì ?", 
        #                     "Chỉ xét trong năm 2022, không xét các năm khác, Ngân hàng An Bình có các sự kiện quan trọng nào?", 
        #                         ] 
                               question_list ))
    return result
    
    