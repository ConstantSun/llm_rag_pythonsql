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



# # global constants
# STREAMLIT_SESSION_VARS: List[Tuple] = [("generated", []), ("past", []), ("input", ""), ("stored_session", [])]
# HTTP_OK: int = 200

# # two options for the chatbot, 1) get answer directly from the LLM
# # 2) use RAG (find documents similar to the user query and then provide
# # those as context to the LLM).
# MODE_RAG: str = 'RAG'
# MODE_TEXT2TEXT: str = 'Text Generation'
# MODE_VALUES: List[str] = [MODE_RAG, MODE_TEXT2TEXT]

# # Currently we use the flan-t5-xxl for text generation
# # and gpt-j-6b for embeddings but in future we could support more
# TEXT2TEXT_MODEL_LIST: List[str] = ["Claude V2"]
# EMBEDDINGS_MODEL_LIST: List[str] = ["infloat"]


####################
# Streamlit code
####################

# Page title
st.set_page_config(page_title='Virtual assistant for knowledge base 👩‍💻', layout='wide')

# keep track of conversations by using streamlit_session
# _ = [st.session_state.setdefault(k, v) for k,v in STREAMLIT_SESSION_VARS]

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


# # sidebar with options
# with st.sidebar.expander("⚙️", expanded=True):
#     text2text_model = st.selectbox(label='Text2Text Model', options=TEXT2TEXT_MODEL_LIST)
#     embeddings_model = st.selectbox(label='Embeddings Model', options=EMBEDDINGS_MODEL_LIST)
#     mode = st.selectbox(label='Mode', options=MODE_VALUES)
    

# streamlit app layout sidebar + main panel
# the main panel has a title, a sub header and user input textbox
# and a text area for response and history
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
    #use an empty container for streaming output
    st_callback = StreamlitCallbackHandler(st.container())
    streaming_response = qna.main(user_question=input_text, streaming_callback=st_callback)



# # download the chat history
# download_str: List = []
# with st.expander("Conversation", expanded=True):
#     for i in range(len(st.session_state['generated'])-1, -1, -1):
#         st.info(st.session_state["past"][i],icon="❓") 
#         st.success(st.session_state["generated"][i], icon="👩‍💻")
#         download_str.append(st.session_state["past"][i])
#         download_str.append(st.session_state["generated"][i])
    
#     # download_str = '\n'.join(download_str)
#     download_str = [x for x in download_str if x is not None] 
#     download_str = '\n'.join(download_str)    
#     if download_str:
#         st.download_button('Download', download_str)