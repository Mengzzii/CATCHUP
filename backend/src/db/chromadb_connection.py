import os
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from .vector_connection import resource, collection_material

from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

directory = ""

# 1. PDF reader
def load_docs(directory, num):
    num_docs = num+".pdf"
    pdf_path = os.path.join(directory, num_docs)
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    return docs

### 2. text split
def split_docs(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 2000, chunk_overlap = 400)
    documents = text_splitter.split_documents(docs)
    return documents

def split_page_contents(documents):
    text_docs = []
    for document in documents:
        page_content = document.page_content
        text_docs.append(page_content)
    return text_docs

## 3. Vector Embedding and Vector Store
def vectordb_store():
    for i in range(1,25):
        docs = load_docs(directory, str(i))
        documents = split_docs(docs)
        text_docs = split_page_contents(documents)

        ids = [f"{i}_{j}" for j in range(len(text_docs))]
        metadatas = [{"catagory": ""} for k in range(len(text_docs))]
        resource.add(
            documents = text_docs,
            ids = ids,
            metadatas = metadatas
        )
        # print(str(i)+"의 embedding: "+str(len(text_docs)))
    return resource

# vectordb_store()

def chromadb_main(concept):
    query = concept

    results_count = 4
    result = resource.query(
    query_texts = [query],
    n_results = results_count
    )

    document_content = ""
    if result and 'documents' in result:
        documents = result['documents']
        for i in range(results_count):
            document_content += documents[0][i] + "\n"
    else:
        print("no result")

    return document_content

# result = chromadb_main("""""")
# print(result)

