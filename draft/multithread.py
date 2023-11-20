from multiprocessing import Pool
# import bedrock 
import time

# def f(question:str):
#     print("start ...................")
#     t1 = time.time()
#     ans1 = bedrock.llm(question)
#     t2 = time.time()
#     print(f'Total time: {t2 - t1:.2f} secs')
#     print("end ...................")
#     return ans1

# def main():
#     with Pool(6) as p:
#         result = (p.map(f, ["tell me about Vietnam, less than 5 sentences.", "tell me about Singapore, less than 5 sentences.", "tell me about Thailand, less than 5 sentences.", "tell me about Malaysia, less than 5 sentences."] ))
#     print("result: -------\n", result)
    
a, b, c = ["hello", "world", "hang"]
print(a)
print(b)
print(c)