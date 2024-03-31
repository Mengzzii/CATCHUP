#chroma DB 연결 & collection 생성
import chromadb

from dotenv import load_dotenv
import os
load_dotenv()

chroma_vm_public_ip = os.environ.get("CHROMA_DB_IP")


chroma_client = chromadb.HttpClient(host= chroma_vm_public_ip, port=8000)

collection = chroma_client.get_or_create_collection(name="test")

collection = chroma_client.get_collection(name="test")

collection.add(
    documents=["This is a document about cat", "This is a document about car"],
    metadatas=[{"category": "animal"}, {"category": "vehicle"}],
    ids=["id1", "id2"]
)

result = collection.query(
    query_texts=["bike"],
    n_results=1
)

print(result)