import single_task.code_flow as code_flow
import question_type
from datetime import datetime


def main():

    # user_question = "RSI của mã Chứng khoán DVN trong 14 ngày gần nhất ?"  # ok, need to combine ans
    # user_question = "Chỉ báo của mã ABB dạo này thế nào?" # ok all ---- error 
    # user_question = "Công ty chứng khoán của bạn có những dịch vụ gì?"  # ok, need to combine ans
    # user_question = "Cổ phiếu mã JKL có biến động thế nào trong tháng 10?" # ok, need to combine ans ---
    # user_question = "Tôi muốn biết thông tin về mã chứng khoán ABB của Ngân hàng thương mại cổ phần An Bình trong năm 2022? " # ok, need to combine ans ---
    user_question = "Cho tôi thông tin chỉ báo AD của mã VCB?"

    start_time = datetime.now()
    user_qstn_type = question_type.get_question_type(user_question)
    print("_____@TIME EXECUTED_____user_qstn_type: ", datetime.now() - start_time)
    if user_qstn_type == "unknown":
        print("unknow user question type")
        return
    
    print(" -------------------user question type: ", user_qstn_type)

    answer = ""
    if user_qstn_type == "1":
        answer = question_type.get_answer_type_1(user_question, start_time)
    elif user_qstn_type == "2":
        answer = question_type.get_answer_type_2(user_question, start_time)
    else:
        answer = question_type.get_answer_type_0(user_question, start_time)

    
    # res = code_flow.test_ask_python_code("Chỉ số EMA cho 14 ngày của mã ABB là gì ?")
    # res = code_flow.test_ask_python_code("RSI của mã Chứng khoán DVN trong 14 ngày gần nhất")
    # res = code_flow.ask_python_code("Chỉ số SMA cho 14 ngày của mã ABB ")
    # res = code_flow.ask_python_code("Cho tôi thông tin chỉ báo AD của mã VCB?")

    print(">>>>>>>>>>>>>>>>>>>>>>\nFINAL ANSWER: ", answer)
    print("_____@TIME EXECUTED_____final: ", datetime.now() - start_time)

main()

# res = code_flow.test_ask_python_code("RSI của mã Chứng khoán DVN trong 14 ngày gần nhất")
# print("____res:____")
# print(res)
