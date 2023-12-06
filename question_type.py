import single_task.code_flow as code_flow
import single_task.rag_flow as rag_flow
import bedrock
from datetime import datetime
from single_task import multi_thread

from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st

# Classifiy question type, currently there are 3 types: Type 1, Type 2, Type 0(other type)
# Answer question corresponding to the question type.


# def get_classify_question_type_prompt(question: str) ->str:
#     '''
#     Classifiy question type, currently there are 3 types: Type 1, Type 2, Type 0(other type)

#     '''
#     return f"""Bạn cần tìm ra câu hỏi dưới đây (là từ một người chơi chứng khoán) có thuộc mẫu câu hỏi nào trong 2 mẫu câu hỏi dưới đây không, các giá trị trong dấu <> có thể được chỉ định cụ thể bởi người dùng :
# Mẫu câu hỏi số 1: Chỉ báo của mã <tên mã> dạo này thế nào?
# Mẫu câu hỏi số 2: Thông tin về mã chứng khoán <tên mã> trong năm 2022? 

# Biết rằng:
# - Nếu hỏi dạng mẫu câu hỏi số 1, có nghĩa là muốn hỏi thông tin chung chung chỉ báo của mã <tên mã> trong thời gian gần đây (hay dạo này), và không hỏi cụ thể chỉ báo nào. Nếu hỏi cụ thể về một chỉ báo <tên chỉ báo> thì câu hỏi đó sẽ không thuộc mẫu câu hỏi số 1. Nếu hỏi cụ thể về thời gian, ví dụ : trong năm 2022, trong tháng 1, trong ngày 3 tháng 5, vân vân, thì câu hỏi sẽ không thuộc mẫu câu hỏi số 1.
# - Nếu hỏi dạng mẫu câu hỏi số 2, có nghĩa là muốn hỏi thông tin chung về mã chứng khoán tên là <tên mã> trong thời gian là năm 2022. Nếu hỏi cụ thể về một hay nhiều thông tin nào đó của mã chứng khoán <tên mã> thì câu hỏi đó sẽ không thuộc mẫu câu hỏi số 2. Nếu hỏi vào thời gian khác năm 2022, ví dụ: hỏi năm 2021, hay năm 2020, vân vân, thì câu hỏi không thuộc mẫu câu hỏi số 2.

# Đây là câu hỏi bạn cần trả lời dựa trên các thông tin ở trên: 
# Câu hỏi: {question}
# Trả lời: Bạn hãy giải thích câu trả lởi và "Kết luận" theo mẫu : 1 nếu Thuộc mẫu câu hỏi số 1, 2 nếu Thuộc mẫu câu hỏi số 2, 0 nếu Không thuộc mẫu câu nào"""


# def get_question_type(question: str) -> str:
#     '''
#     Return question type: 0,1,2 or unknown.
#     '''
#     prompt = get_classify_question_type_prompt(question)
#     answer = bedrock.ask_direct(prompt)
#     print("get_question_type answer:\n", answer)
#     for line in answer.splitlines():
#         line = line.lower()
#         if "kết luận" in line[:10]:
#             if "không thuộc" in line or "0" in line:
#                 return "0"
#             elif "1" in line:
#                 return "1"
#             elif "2" in line:
#                 return "2"
#             else:
#                 print("inline: unknow question type")
#                 return "unknown"
#     print("overall: unknown question type")
#     return "unknown"








def get_classify_question_type_prompt(question: str) ->str:
    '''
    Classifiy question type, currently there are 3 types: Type 1, Type 2, Type 0(other type)

    '''
    return f"""Bạn cần tìm ra câu hỏi dưới đây (là từ một người chơi chứng khoán) có thuộc mẫu câu hỏi nào trong 2 mẫu câu hỏi dưới đây không, các giá trị trong dấu <> có thể được chỉ định cụ thể bởi người dùng :
Mẫu câu hỏi số 1: Chỉ báo của mã <tên mã> dạo này thế nào?
Mẫu câu hỏi số 2: Thông tin về mã chứng khoán <tên mã> trong năm 2022? 

Biết rằng:
- Nếu hỏi dạng mẫu câu hỏi số 1, có nghĩa là muốn hỏi thông tin chung chung chỉ báo của mã <tên mã> trong thời gian gần đây (hay dạo này), và không hỏi cụ thể chỉ báo nào. Nếu hỏi cụ thể về một chỉ báo <tên chỉ báo> thì câu hỏi đó sẽ không thuộc mẫu câu hỏi số 1. Nếu hỏi cụ thể về thời gian, ví dụ : trong năm 2022, trong tháng 1, trong ngày 3 tháng 5, vân vân, thì câu hỏi sẽ không thuộc mẫu câu hỏi số 1.
- Nếu hỏi dạng mẫu câu hỏi số 2, có nghĩa là muốn hỏi thông tin chung về mã chứng khoán tên là <tên mã> trong thời gian là năm 2022. Nếu hỏi cụ thể về một hay nhiều thông tin nào đó của mã chứng khoán <tên mã> thì câu hỏi đó sẽ không thuộc mẫu câu hỏi số 2. Nếu hỏi vào thời gian khác năm 2022, ví dụ: hỏi năm 2021, hay năm 2020, vân vân, thì câu hỏi không thuộc mẫu câu hỏi số 2.

Một vài ví dụ như sau:

Câu hỏi sau đây thuộc loại nào?
Chỉ báo của mã ABC dạo này thế nào?
Trả lời: 1

Câu hỏi sau đây thuộc loại nào?
Thông tin về mã chứng khoán XYZ trong năm 2020?
Trả lời: 2

Câu hỏi sau đây thuộc loại nào?
Thời tiết hôm nay thế nào?
Trả lời: 0

Không giải thích, không nói thêm những câu "Dựa trên thông tin cung cấp" hay tương tự.
Chỉ trả về số tương ứng loại câu hỏi, không giải thích thêm thông tin gì khác, trả lời ngắn gọn nhất có thể.
Câu hỏi sau đây thuộc loại nào? 
{question}
Trả lời:"""



def get_answer_from_line(line: str):
    if "không thuộc" in line or "0" in line:
        return "0"
    elif "1" in line:
        return "1"
    elif "2" in line:
        return "2"
    else:
        print("inline: unknow question type")
        return "unknown"

def get_question_type(question: str) -> str:
    '''
    Return question type: 0,1,2 or unknown.
    '''
    prompt = get_classify_question_type_prompt(question)
    answer = bedrock.ask_direct(prompt, max_tokens_to_sample=150)
    print("get_question_type answer:\n", answer)

    lines = answer.splitlines()

    # Get direct answer if the answer is short
    if len(lines) == 1:
        return get_answer_from_line(lines[0])
    # Else try to get long answer
    for line in lines:
        line = line.lower()
        if "trả lời" in line[:10]:
            return get_answer_from_line(line)
    print("overall: unknown question type")
    return "unknown"



def get_stock_code(question: str) -> str:
    prompt = f"""Mã cổ phiếu nào được đề cập trong câu hỏi sau, chỉ cần trả lời tên mã, không cần giải thích gì thêm: "{question}" """
    stock_code = bedrock.ask_short(prompt)
    return stock_code.upper()

def get_bank_name(question:str) -> str:
    prompt = f"""Ngân hàng hay Công ty nào được đề cập trong câu hỏi sau, chỉ cần trả lời tên Ngân hàng hoặc Công ty đó, không cần giải thích gì thêm: "{question}" """    
    name = bedrock.ask_short(prompt)
    return name

def get_answer_type_1(question, start_time):
    '''
    Hỏi thông tin chung chung chỉ báo của mã <tên mã> trong thời gian gần đây
    '''
    stock_code = get_stock_code(question)

    question_list = [[code_flow.ask_python_code, (f"Chỉ số RSI của mã {stock_code} là gì?", )], 
                     [code_flow.ask_python_code,( f"Chỉ số SMA của mã {stock_code} là gì?",)],
                     [code_flow.ask_python_code,( f"Chỉ số EMA của mã {stock_code} cho 14 ngày là gì?", )]]
    rsi, sma, ema = multi_thread.run_multi_funcs(question_list)

    ans = f"""Dựa trên dữ liệu gần nhất cho mã chứng khoán {stock_code}:
- Chỉ số RSI là {rsi[0]}.
- Chỉ số SMA cho 14 ngày là {sma[0]}.
- Chỉ số EMA cho 14 ngày là {ema[0]}."""
    return ans

def get_answer_type_2(question, start_time):
    '''
    Thông tin về mã chứng khoán <tên mã> trong năm 2022?
    '''
    # stock_code = "ABB"
    # bank_name = "Ngân hàng TMCP An Bình"

    stock_code, bank_name = None, None
    stock_code, bank_name = multi_thread.run_multi_funcs([ [get_stock_code, (question,)], [get_bank_name, (question,)] ])
    if stock_code is None or "xin lỗi" in stock_code.lower():
        return "type 2 processing error, in stock_code detect"
    if bank_name is None or "xin lỗi" in bank_name.lower():
        return "type 2 processing error, in bank_name detect"


    st_callback_1 = StreamlitCallbackHandler(st.container())
    st_callback_2 = StreamlitCallbackHandler(st.container())

    question_list = [
        [code_flow.ask_python_code, (f"Mã {stock_code} có mức giá đóng cửa trung bình trong năm 2022 cao hơn bao nhiêu phần trăm so với mức giá đóng cửa trung bình trong năm 2021 ?",)],
        [rag_flow.ask_streaming_rag, (st_callback_1 ,f"Trong năm 2022, {bank_name} có các sự kiện quan trọng nào?")],
        [rag_flow.ask_streaming_rag, (st_callback_2 ,f"Trong năm 2022, {bank_name} đạt được những giải thưởng gì ?")]
    ]

    percentage, rag_answer_1, rag_answer_2 = multi_thread.run_multi_funcs(question_list)
    print("percentage:", percentage)
    print("rag_answer_1:", rag_answer_1)
    print("rag_answer_2:", rag_answer_2)
    print("<3 "*60)
#     ans = f"""Mã {stock_code} có mức giá đóng cửa trung bình trong năm 2022 cao hơn {percentage} phần trăm so với năm 2021.
# Trong năm 2022, {bank_name} cũng có các sự kiện quan trọng sau: \n{rag_answer_1}

# Đồng thời cũng trong năm 2022, Ngân hàng TMCP An Bình đạt được những giải thưởng sau:\n{rag_answer_2}"""

    ans = f"""Mã {stock_code} có mức giá đóng cửa trung bình trong năm 2022 cao hơn {percentage} phần trăm so với năm 2021."""
    return ans


def get_answer_type_0(question, start_time):
    st_callback = StreamlitCallbackHandler(st.container())
    rag_answer, code_answer = multi_thread.run_multi_funcs([ [rag_flow.ask_streaming_rag, (st_callback, question)] , 
                                                             [code_flow.ask_python_code, ( question,) ]
                                                           ])
    # if len(code_answer) == 0 or code_answer[0] == "no query result" or str(code_answer) == "0" or str(code_answer) == "[0]" :
    #     if "Đang xử lý ..." in rag_answer:
    #         res = "Hiện tại chưa có thông tin về mã chứng khoán của quý khách. Vui lòng xem thêm tại đường link sau: https://itrade.abs.vn/"
    #         st.text(res)
    #         return res
    if "_end_" in code_answer and "..." == rag_answer.strip():
        st.text("Xin lỗi, tôi không trả lời được câu hỏi này.")
    return "rag_answer:\n" + "$" + rag_answer + "$" + "\n--------\n" + "code_answer:\n" + code_answer

