import asyncio
import time
import bedrock

async def func1():
    print('func1 start')
    ans1 = bedrock.llm("tell me about Vietnam, less than 5 sentences.")
    print('func1 end: ', ans1 )

async def func2():
    print('func2 start')
    ans2 = bedrock.llm("tell me about Singapore, less than 5 sentences.")
    print('func2 end', ans2)

async def func3():
    print('func3 start')
    await asyncio.sleep(4)  
    print('func3 end')

async def main():
    await asyncio.gather(
        func1(),
        func2(),
        func3()
    )

# def main():
#     t1 = time.time()
#     asyncio.run(main())
#     t2 = time.time()
#     print(f'Total time: {t2 - t1:.2f} secs')