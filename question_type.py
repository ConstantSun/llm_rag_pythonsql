import single_task.code_flow as code_flow
import single_task.rag_flow as rag_flow
import bedrock
from datetime import datetime

# Classifiy question type, currently there are 3 types: Type 1, Type 2, Type 0(other type)
# Answer question corresponding to the question type.


def get_classify_question_type_prompt(question: str) ->str:
    '''
    Classifiy question type, currently there are 3 types: Type 1, Type 2, Type 0(other type)

    '''
    return f"""Bạn cần tìm ra câu hỏi dưới đây (là từ một người chơi chứng khoán) có thuộc mẫu câu hỏi nào trong 2 mẫu câu hỏi dưới đây không, các giá trị trong dấu <> có thể được chỉ định cụ thể bởi người dùng :
Mẫu câu hỏi số 1: Chỉ báo của mã <tên mã> dạo này thế nào?
Mẫu câu hỏi số 2: Thông tin về mã chứng khoán <tên mã> trong năm 2022? 

Biết rằng:
- Nếu hỏi dạng mẫu câu hỏi số 1, có nghĩa là muốn hỏi thông tin chung chung chỉ báo của mã <tên mã> trong thời gian gần đây (hay dạo này), và không hỏi cụ thể chỉ báo nào. Nếu hỏi cụ thể về một chỉ báo <tên chỉ báo> thì câu hỏi đó sẽ không thuộc mẫu câu hỏi số 1. Nếu hỏi cụ thể về thời gian, ví dụ : trong năm 2022, trong tháng 1, trong ngày 3 tháng 5, vân vân, thì câu hỏi sẽ không thuộc mẫu câu hỏi số 1.
- Nếu hỏi dạng mẫu câu hỏi số 2, có nghĩa là muốn hỏi thông tin chung chung về mã chứng khoán <tên mã> trong thời gian là năm 2022, và không hỏi cụ thể về thông tin nào. Nếu hỏi cụ thể về một hay nhiều thông tin nào đó của mã chứng khoán <tên mã> thì câu hỏi đó sẽ không thuộc mẫu câu hỏi số 2. Nếu hỏi vào thời gian khác năm 2022, ví dụ: hỏi năm 2021, hay năm 2020, vân vân, thì câu hỏi không thuộc mẫu câu hỏi số 2.

Đây là câu hỏi bạn cần trả lời dựa trên các thông tin ở trên: 
Câu hỏi: {question}
Trả lời: Bạn hãy giải thích câu trả lởi và "Kết luận" theo mẫu : 1 nếu Thuộc mẫu câu hỏi số 1, 2 nếu Thuộc mẫu câu hỏi số 2, 0 nếu Không thuộc mẫu câu nào"""


def get_question_type(question: str) -> str:
    '''
    Return question type: 0,1,2 or unknown.
    '''
    prompt = get_classify_question_type_prompt(question)
    answer = bedrock.llm(prompt)
    print("get_question_type answer:\n", answer)
    for line in answer.splitlines():
        line = line.lower()
        if "kết luận" in line[:10]:
            if "không thuộc" in line or "0" in line:
                return "0"
            elif "1" in line:
                return "1"
            elif "2" in line:
                return "2"
            else:
                print("inline: unknow question type")
                return "unknown"
    print("overall: unknown question type")
    return "unknown"


def get_stock_code(question: str) -> str:
    prompt = f"""Mã nào được đề cập trong câu hỏi sau, chỉ cần trả lời tên mã, không cần giải thích gì thêm: "{question}" """
    stock_code = bedrock.llm(prompt)
    return stock_code.upper()

def get_bank_name(question:str) -> str:
    prompt = f"""Ngân hàng hay Công ty nào được đề cập trong câu hỏi sau, chỉ cần trả lời tên Ngân hàng hoặc Công ty đó, không cần giải thích gì thêm: "{question}" """
    name = bedrock.llm(prompt)
    return name

def get_answer_type_1(question, start_time):
    '''
    Hỏi thông tin chung chung chỉ báo của mã <tên mã> trong thời gian gần đây
    '''
    stock_code = get_stock_code(question)

    # Run 3 instructions in parallel:
    rsi = code_flow.ask_python_code(f"Chỉ số RSI của mã {stock_code} là gì?")
    sma = code_flow.ask_python_code(f"Chỉ số SMA của mã {stock_code} cho 14 ngày là gì?")
    ema = code_flow.ask_python_code(f"Chỉ số EMA của mã {stock_code} cho 14 ngày là gì?")
    
    ans = f"""Dựa trên dữ liệu gần nhất cho mã chứng khoán {stock_code}:
- Chỉ số RSI là {rsi[0]}.
- Chỉ số SMA cho 14 ngày là {sma[0]}.
- Chỉ số EMA cho 14 ngày là {ema[0]}."""
    return ans

def get_answer_type_2(question, start_time):
    '''
    Thông tin về mã chứng khoán <tên mã> trong năm 2022?
    '''
    stock_code = get_stock_code(question)
    
    # Run 2 instructions in parallel:
    percentage = code_flow.ask_python_code(f"Mã {stock_code} có mức giá đóng cửa trung bình trong năm 2022 cao hơn bao nhiêu phần trăm so với mức giá đóng cửa trung bình trong năm 2021 ?")
    
    bank_name = get_bank_name(question)
    rag_answer = rag_flow.ask_rag(f"Chỉ xét trong năm 2022, không xét các năm khác, {bank_name} có các sự kiện quan trọng nào ?")
    
    ans = f"""Mã {stock_code} có mức giá đóng cửa trung bình trong năm 2022 cao hơn {percentage} phần trăm so với năm 2021.
Trong năm 2022, {bank_name} cũng có các sự kiện quan trọng sau: \n{rag_answer}"""
    return ans


def get_answer_type_0(question, start_time):

    rag_answer = rag_flow.ask_rag(question)
    print(f"_____@TIME EXECUTED_____RAG ANSWER______: {datetime.now() - start_time} \n", rag_answer)
    code_answer = code_flow.ask_python_code(question, start_time)
    print(f"_____@TIME EXECUTED_____CODE ANSWER_____: {datetime.now() - start_time} \n", code_answer)
    return "rag_answer:\n" + rag_answer + "\n--------\n" + "code_answer:\n" + code_answer