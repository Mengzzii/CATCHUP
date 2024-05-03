import os
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from .vector_connection import collection_material
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

directory = ""

## 1. PDF reader
def load_docs(directory):
    loader = PyPDFLoader(directory+"")
    docs = loader.load()
    return docs

### 2. text split
def split_docs(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 400)
    documents = text_splitter.split_documents(docs)
    return documents

### 3. Vector Embedding and Vector Store
def vectordb_store():
    docs = load_docs(directory)
    documents = split_docs(docs)
    embeddings = OpenAIEmbeddings()
    # db = Chroma.from_documents(documents, embeddings)

    persist_directory = "chroma_db"
    vectordb = Chroma.from_documents(
        documents = documents, embedding = embeddings, persist_directory = persist_directory
    )
    vectordb.persist()
    return vectordb

def chromadb_main(concept):
    query = concept

    result = collection_material.query(
    query_texts=[query],
    n_results=1
    )

    if result and 'documents' in result:
        documents = result['documents']
        document_content = documents[0][0]

    return document_content