from dotenv import load_dotenv
import os
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate

load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")

# YOUTUBE_VIDEO = "https://www.youtube.com/watch?v=cdiD-9MMpb0"
model = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo")
parser = StrOutputParser()

template = """
Answer the question based on the context below. If you can't 
answer the question, reply "I don't know".

Context: {context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model | parser
result = chain.invoke({
    "context": "Mary's sister is Susana",
    "question": "Who is Mary's sister?"
})

print(result)

with open("transcription.txt") as file:
    transcription = file.read()

transcription[:100]
#loading the transcription in memory
from langchain_community.document_loaders import TextLoader

loader = TextLoader("transcription.txt")
text_documents = loader.load()
text_documents