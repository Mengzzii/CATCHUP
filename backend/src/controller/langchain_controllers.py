from dotenv import load_dotenv
import os
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings


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

# with open("C:/Users/cse/Desktop/catchup19/CATCHUP/transcription.txt") as file:
#     transcription = file.read()
# res = transcription[:100]
# print(res)

#loading the transcription in memory
loader = TextLoader("C:/Users/cse/Desktop/catchup19/CATCHUP/transcription.txt")
text_documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=10, chunk_overlap=2)
res = text_splitter.split_documents(text_documents)

embeddings = OpenAIEmbeddings()
embedded_query = embeddings.embed_query("Who is Mary's sister?")

print(f"Embedding length: {len(embedded_query)}")
print(embedded_query[:10])