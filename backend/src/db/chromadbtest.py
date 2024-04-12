# import os
# from langchain.chat_models import ChatOpenAI
# from langchain.document_loaders import DirectoryLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import SentenceTransformerEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.chains.question_answering import load_qa_chain
# from langchain.chains import RetrievalQA

# directory = '/content/pets'

# def load_docs(directory):
#   loader = DirectoryLoader(directory)
#   documents = loader.load()
#   return documents

# def split_docs(documents):
#   chunk_size=1000
#   chunk_overlap=20
#   text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#   docs = text_splitter.split_documents(documents)
#   return docs

# documents = load_docs(directory)
# docs = split_docs(documents)
# embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# db = Chroma.from_document(docs, embeddings)

# query = "What are the different kinds of pets people commonly own?"
# matching_docs = db.similarity_search(query)

# matching_docs[0]

# persist_directory = "chroma_db"

# vectordb = Chroma.from_documents(
#     documents=docs, embedding=embeddings, persist_directory=persist_directory
# )

# vectordb.persist()

# os.environ["OPENAI_API_KEY"] = "key"

# model_name = "gpt-3.5-turbo"
# llm = ChatOpenAI(model_name=model_name)

# chain = load_qa_chain(llm, chain_type="stuff",verbose=True)

# query = "What are the emotional benefits of owning a pet?"
# matching_docs = db.similarity_search(query)
# answer =  chain.run(input_documents=matching_docs, question=query)
# answer

# retrieval_chain = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=db.as_retriever())
# retrieval_chain.run(query)

import os
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

### 1. Load Source Data
## Data Ingestion
from langchain_community.document_loaders import TextLoader
loader = TextLoader("test.txt")
text_documents1 = loader.load()

## Web based loader
from langchain_community.document_loaders import WebBaseLoader
import bs4

## load, chunk and index the content of the html page
loader = WebBaseLoader(web_paths = "https://aws.amazon.com/ko/what-is/langchain/",
                       bs_kwargs = dict(parse_only = bs4.SoutStrainer(
                           class_=("post_title", "post_content", "post_header")
                       )))
text_documents2 = loader.load

## PDF reader
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("Lecture 6.pdf")
docs = loader.load

### 2. text split
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
documents = text_splitter.split_documents(docs)

### 3. Vector Embedding and Vector Store
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
db = Chroma.from_documents(documents[:15], OpenAIEmbeddings())


### 4. Vector Database
query = ""
result = db.similarity_search(query)
result[0].page_content

## +) FAISS Vector Database
from langchain_community.vectorstores import FAISS
db2 = FAISS.from_documents(documents[:20], OpenAIEmbeddings())
query = ""
result = db2.similarity_search(query)
result[0].page_content
