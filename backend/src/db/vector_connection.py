import chromadb
from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings()

# ChromaDB 연결
chroma_vm_public_ip = os.environ.get("CHROMA_DB_IP")
chroma_client = chromadb.HttpClient(host=chroma_vm_public_ip, port=8000)
vector_store = Chroma(embedding_function=embeddings)
collection_material = chroma_client.get_or_create_collection(name="material")