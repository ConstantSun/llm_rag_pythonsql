from multiprocessing import Pool
import bedrock 
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
    
# a, b, c = ["hello", "world", "hang"]
# print(a)
# print(b)
# print(c)

# from threading import Thread

# list1, list2 = [], []

# def func1(x):
#     print("start ...................")
#     t1 = time.time()
#     global list1
#     ans1 = bedrock.llm("tell me about Vietnam, less than 5 sentences.")
#     list1 = [ans1]
#     print(f'Total time - Vietnam: {time.time() - t1:.2f} secs')

# def func2(x):
#     print("start ...................")
#     t1 = time.time()    
#     global list2
#     ans2 = bedrock.llm("tell me about Singapore, less than 5 sentences.")
#     list2 = [ans2]
#     print(f'Total time - Singapore: {time.time() - t1:.2f} secs')

# def main():
#     nums = [1,2,3,4,5]

#     Thread(target = func1, args=(nums,)).start()
#     Thread(target = func2, args=(nums,)).start()

#     print(list1, list2)










from threading import Thread
from queue import Queue

def func1(x):
    print("start ...................")
    t1 = time.time()
    ans1 = bedrock.llm("tell me about Vietnam, less than 5 sentences.")
    print(f'Total time - Vietnam: {time.time() - t1:.2f} secs')

    return [ans1]

def func2(x):
    print("start ...................")
    t1 = time.time()
    ans2 = bedrock.llm("tell me about Singapore, less than 5 sentences.")
    print(f'Total time - singapore: {time.time() - t1:.2f} secs')

    return [ans2]

nums = [1,2,3,4,5]

def wrapper(func, arg, queue):
    queue.put(func(arg))

# def main():
#     q1, q2 = Queue(), Queue()
#     Thread(target=wrapper, args=(func1, nums, q1)).start() 
#     Thread(target=wrapper, args=(func2, nums, q2)).start() 

#     print(q1.get(), q2.get())






import threading 
import queue

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


def worker(func, args, results):
    results.put(func(*args))
    
def main():    
    q = queue.Queue()

    threads = []
    t1 = threading.Thread(target=worker, args=(func1, (1,2,3), q))  
    threads.append(t1)
    t2 = threading.Thread(target=worker, args=(func2, (4, 5), q))
    threads.append(t2) 
    t3 = threading.Thread(target=worker, args=(func3, (6, 7, 8), q))  
    threads.append(t3)

    for t in threads:
        t.start()

    results = [] 
    for t in threads: 
        t.join()
        results.append(q.get())

    print(results)   