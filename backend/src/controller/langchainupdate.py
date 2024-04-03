# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser

# import streamlit as st

# os.environ["OPEN_API_KEY"] = os.getenv("OPEN_API_KEY")
# os.environ["LANCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# ## Prompt Template

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are a helpful assistant. Please response to the user queries")
#         ("user","Question: {question}")
#     ]
# )

# ## Streamlit framework
# st.title("Langchain Demo With OPENAI API")
# input_text = st.text_input("Search the topic you want")

# ## OpenAI LLM
# llm = ChatOpenAI(model="gpt-3.5-turbo")
# output_parser = StrOutputParser()
# chain = prompt | llm | output_parser

# if input_text:
