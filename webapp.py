"""
A simple web application to implement a chatbot. This app uses Streamlit 
for the UI and the Python requests package to talk to an API endpoint that
implements text generation and Retrieval Augmented Generation (RAG) using LLMs
and Amazon OpenSearch as the vector database.
"""
import streamlit as st
import qna  


# Page title
st.set_page_config(page_title='Virtual assistant for knowledge base 👩‍💻', layout='wide')
st.title("👩‍💻 Virtual Assistant")
# st.subheader(f" Powered by :blue[{TEXT2TEXT_MODEL_LIST[0]}] for text generation and :blue[{EMBEDDINGS_MODEL_LIST[0]}] for embeddings")

st.subheader(f"Powered by AWS x ABS")

input_text = st.text_area("Input text", label_visibility="collapsed")
go_button = st.button("Go", type="primary")  # display a primary button

if go_button:  # code in this if block will be run when the button is clicked
    streaming_response: str = None
    streaming_response = qna.main(user_question=input_text)

