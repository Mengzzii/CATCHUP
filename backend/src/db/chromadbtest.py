import os
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

# ### 1. Load Source Data
# ## Data Ingestion
# from langchain_community.document_loaders import TextLoader
# loader = TextLoader("test.txt")
# text_documents1 = loader.load()

# ## Web based loader
# from langchain_community.document_loaders import WebBaseLoader
# import bs4

# ## load, chunk and index the content of the html page
# loader = WebBaseLoader(web_paths = "https://aws.amazon.com/ko/what-is/langchain/",
#                        bs_kwargs = dict(parse_only = bs4.SoutStrainer(
#                            class_=("post_title", "post_content", "post_header")
#                        )))
# text_documents2 = loader.load


directory = "c:\\Users\\믕지\\OneDrive\\바탕 화면\\workout\\CATCHUP\\backend\\src\\data"

## 1. PDF reader
def load_docs(directory):
    loader = PyPDFLoader(directory+"\\2. Data Structure.pdf")
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

    # collection.add(
#     documents=["This is a document about cat", "This is a document about car"],
#     metadatas=[{"category": "animal"}, {"category": "vehicle"}],
#     ids=["id1", "id2"]
#   )
    persist_directory = "chroma_db"
    vectordb = Chroma.from_documents(
        documents = documents, embedding = embeddings, persist_directory = persist_directory
    )
    vectordb.persist()
    return vectordb

from .vector_connection import collection
def chromadb_main(concept):
    query = concept

    result = collection.query(
    query_texts=[query],
    n_results=1
    )

    if result and 'documents' in result:
        documents = result['documents']
        document_content = documents[0][0]

    return document_content