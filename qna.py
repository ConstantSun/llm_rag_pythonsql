import single_task.code_flow as code_flow
import question_type

def main():
    user_question = "Cho tôi thông tin chỉ báo AD của mã VCB?"
    user_qstn_type = question_type.get_question_type(user_question)
    if user_qstn_type == "unknown":
        print("unknow user question type")
        return
    
    print(" -----1--------------\nuser question type: ", answer)

    answer = ""
    # if user_qstn_type == "1":
    #     answer = question_type.get_answer_type_1(user_question)
    # elif user_qstn_type == "2":
    #     answer = question_type.get_answer_type_2(user_question)
    # else:
    #     answer = question_type.get_answer_type_0(user_question)

    
    # res = code_flow.test_ask_python_code("Chỉ số EMA cho 14 ngày của mã ABB là gì ?")
    # res = code_flow.test_ask_python_code("RSI của mã Chứng khoán DVN trong 14 ngày gần nhất")
    # res = code_flow.ask_python_code("Chỉ số SMA cho 14 ngày của mã ABB ")
    # res = code_flow.ask_python_code("Cho tôi thông tin chỉ báo AD của mã VCB?")

    print(">>>>>>>>>>>>>>>>>>>>>>\nFINAL ANSWER: ", answer)

main()