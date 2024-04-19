import chromadb
from dotenv import load_dotenv
import os
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings()

chroma_vm_public_ip = os.environ.get("CHROMA_DB_IP")
chroma_client = chromadb.HttpClient(host= chroma_vm_public_ip, port=8000)
vector_store = Chroma(embedding_function=embeddings)
collection = chroma_client.get_or_create_collection(name="test")


## 1. PDF reader
# def load_docs(directory):
#     loader = PyPDFLoader(directory+"\\8. Binary Heaps.pdf")
#     docs = loader.load()
#     return docs

# directory = "c:\\Users\\믕지\\OneDrive\\바탕 화면\\workout\\CATCHUP\\backend\\src\\data"
# ### 2. text split
# def split_docs(docs):
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 300)
#     documents = text_splitter.split_documents(docs)
#     text_documents = []
#     for document in documents:
#         text_documents.append(document.page_content)
#     return text_documents

# ### 3. Vector Embedding and Vector Store
# docs = load_docs(directory)
# documents = split_docs(docs)

# ids = [str(i) for i in range(len(documents))]

# collection.add(
#     documents=documents,
#     ids=ids
# )



# collection = chroma_client.get_collection(name="test")

# collection.add(
#     documents=["This is a document about cat", "This is a document about car"],
#     metadatas=[{"category": "animal"}, {"category": "vehicle"}],
#     ids=["id1", "id2"]
# )

# result = collection.query(
#     query_texts=["array"],
#     n_results=1
# )

# print(result)


# ids = [str(i) for i in range(len(documents))]

# collection.add(
#     documents=documents,
#     ids=ids,
#     embeddings=embeddings
# )


# 크로마에 데이터 add 하는 부분부터 시작

    # persist_directory = "chroma_db"
    # vectordb = Chroma.from_documents
    #     documents = documents, embedding = embeddings, persist_directory = persist_directory
    # )
    # vectordb.persist()
    # return vectordb