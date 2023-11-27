"""
A simple web application to implement a chatbot. This app uses Streamlit 
for the UI and the Python requests package to talk to an API endpoint that
implements text generation and Retrieval Augmented Generation (RAG) using LLMs
and Amazon OpenSearch as the vector database.
"""
import boto3
import streamlit as st
import requests as req
from typing import List, Tuple, Dict
from qna import main
from langchain.callbacks import StreamlitCallbackHandler
import qna  




# Page title
st.set_page_config(page_title='Virtual assistant for knowledge base 👩‍💻', layout='wide')


# Define function to get user input
def get_user_input() -> str:
    """
    Returns the text entered by the user
    """
    print(st.session_state)    
    input_text = st.text_input("You: ",
                               st.session_state["input"],
                               key="input",
                               placeholder="Ask me a question and I will consult the knowledge base to answer...", 
                               label_visibility='hidden')
    return input_text

st.title("👩‍💻 Virtual Assistant")
# st.subheader(f" Powered by :blue[{TEXT2TEXT_MODEL_LIST[0]}] for text generation and :blue[{EMBEDDINGS_MODEL_LIST[0]}] for embeddings")

st.subheader(f"Powered by AWS x ABS")





user_input = ""
# get user input
# user_input: str = get_user_input()

# based on the selected mode type call the appropriate API endpoint
# if user_input:
    # headers for request and response encoding, same for both endpoints
    # headers: Dict = {"accept": "application/json", "Content-Type": "application/json"}
    # output: str = None
    # output = main(user_input)
    # st.session_state.past.append(user_input)  
    # st.session_state.generated.append(output) 


input_text = st.text_area("Input text", label_visibility="collapsed")
go_button = st.button("Go", type="primary")  # display a primary button

if go_button:  # code in this if block will be run when the button is clicked
    streaming_response: str = None
    #use an empty container for streaming output
    st_callback = StreamlitCallbackHandler(st.container())
    streaming_response = qna.main(user_question=input_text, streaming_callback=st_callback)



