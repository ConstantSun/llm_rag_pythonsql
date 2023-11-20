from multiprocessing import Pool
import bedrock
import time

def f(question:str):
    print("start ...................")
    t1 = time.time()
    ans1 = bedrock.llm(question)
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
        result = (p.map(f, question_list ))
    print("result: -------\n", result)
    return result
    
    