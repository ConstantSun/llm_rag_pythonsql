classify_question_type_prompt = """Bạn cần tìm ra câu hỏi dưới đây (là từ một người chơi chứng khoán) có thuộc mẫu câu hỏi nào trong 2 mẫu câu hỏi dưới đây không, các giá trị trong dấu <> có thể được chỉ định cụ thể bởi người dùng :
Mẫu câu hỏi số 1: Chỉ báo của mã <tên mã> dạo này thế nào?
Mẫu câu hỏi số 2: Thông tin về mã chứng khoán <tên mã> trong năm 2022? 

Biết rằng:
- Nếu hỏi dạng mẫu câu hỏi số 1, có nghĩa là muốn hỏi thông tin chung chung chỉ báo của mã <tên mã> trong thời gian gần đây (hay dạo này), và không hỏi cụ thể chỉ báo nào. Nếu hỏi cụ thể về một chỉ báo <tên chỉ báo> thì câu hỏi đó sẽ không thuộc mẫu câu hỏi số 1. Nếu hỏi cụ thể về thời gian, ví dụ : trong năm 2022, trong tháng 1, trong ngày 3 tháng 5, vân vân, thì câu hỏi sẽ không thuộc mẫu câu hỏi số 1.
- Nếu hỏi dạng mẫu câu hỏi số 2, có nghĩa là muốn hỏi thông tin chung chung về mã chứng khoán <tên mã> trong thời gian là năm 2022, và không hỏi cụ thể về thông tin nào. Nếu hỏi cụ thể về một hay nhiều thông tin nào đó của mã chứng khoán <tên mã> thì câu hỏi đó sẽ không thuộc mẫu câu hỏi số 2. Nếu hỏi vào thời gian khác năm 2022, ví dụ: hỏi năm 2021, hay năm 2020, vân vân, thì câu hỏi không thuộc mẫu câu hỏi số 2.

Đây là câu hỏi bạn cần trả lời dựa trên các thông tin ở trên: 
Câu hỏi: Tôi muốn biết thông tin về chỉ số RSI của mã chứng khoán TEE trong năm 2022
Trả lời: Bạn hãy giải thích câu trả lởi và "Kết luận" theo mẫu : 1 nếu Thuộc mẫu câu hỏi số 1, 2 nếu Thuộc mẫu câu hỏi số 2, 0 nếu Không thuộc mẫu câu nào"""

qn_dict = [
{
    question: "Chỉ báo của mã <tên mã> dạo này thế nào?",
    question_type: "1",
    ans: f"""Dựa trên dữ liệu gần nhất cho mã chứng khoán {stock_code}:
- Chỉ số RSI là {rsi_value}.
- Chỉ số SMA cho 14 ngày là {sma_value}.
- Chỉ số EMA cho 14 ngày là {ema_value}."""

},
{
    question: "Thông tin về mã chứng khoán <tên mã> trong năm 2022?",
    question_type: "2",
    ans: f"Mã {stock_code} có mức giá đóng cửa trung bình trong năm 2022 cao hơn {percentage} so với năm 2021. Trong năm 2022, Ngân hàng {bank_name} cũng có các sự kiện quan trọng sau: {rag_answer}"
}
]
