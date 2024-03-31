import os
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA

directory = '/content/pets'

def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents

def split_docs(documents):
  chunk_size=1000
  chunk_overlap=20
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

documents = load_docs(directory)
docs = split_docs(documents)
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma.from_document(docs, embeddings)

query = "What are the different kinds of pets people commonly own?"
matching_docs = db.similarity_search(query)

matching_docs[0]

persist_directory = "chroma_db"

vectordb = Chroma.from_documents(
    documents=docs, embedding=embeddings, persist_directory=persist_directory
)

vectordb.persist()

os.environ["OPENAI_API_KEY"] = "key"

model_name = "gpt-3.5-turbo"
llm = ChatOpenAI(model_name=model_name)

chain = load_qa_chain(llm, chain_type="stuff",verbose=True)

query = "What are the emotional benefits of owning a pet?"
matching_docs = db.similarity_search(query)
answer =  chain.run(input_documents=matching_docs, question=query)
answer

retrieval_chain = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=db.as_retriever())
retrieval_chain.run(query)