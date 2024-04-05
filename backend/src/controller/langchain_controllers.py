import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from operator import itemgetter

from langchain_community.document_loaders import TextLoader
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

contextlist = []
#기본챗방에서 개념리스트 반환용 프롬프트 엔지니어링
# contextlist[0]
contextlist.append("""I'm trying to develop a chatbot tailored to assist struggling computer science students.
                   When a user specifies a subject for study, you should promptly supply a concise yet comprehensive list of relevant concepts. 
                   It is crucial that when presenting these concepts, they are meticulously broken down into granular units, including only the essential components pertinent to the subject matter. 
                   For instance, instead of just listing the terms like "Sorting Algorithms," each algorithm like Bubble Sort, Selection Sort, Merge Sort, Quick Sort, and Radix Sort must be stored separately in db. 
                   Furthermore, please ensure that each concept is prioritized, as we will follow this order for learning purposes. Additionally,  you want to store the provided list into MongoDB using a model called Concept, which includes the fields "name: str" . 
                   So please print out the result in json format to facilitate entering this model.
                      - format: List of JSON
                      - No code block delimiter.
                      - Do not add other comments, only return the list of JSON.
                      - example : [{"name":"concept1"}, {"name":"concept2"},{"name":"concept3"}, ...]"""
                   )
#개념챗방에서 학습자료 제공용 프롬프트 엔지니어링
# contextlist[1]
contextlist.append("""You are a Computer science professor.
                    You will make learning materials based on the given materials and the given concepts.
                    Learning materials should contain enough content for university students to understand, and the amount of content should be made so that the learning can be completed in 30-40 minutes.
                    Most importantly, make the learning material only based on the given documents.
                    Also, arrange the paragraph structure to make it easier for the student to read."""
                    )
#개념챗방에서 사용자 Q&A용 프롬프트 엔지니어링
# contextlist[2]
contextlist.append("""You are a Computer science professor.
                    Please answer the question in as much detail as possible and kindly as possible
                    And please answer the question in context based on the previous chat that is given.
                    Also, sympathize with the student!"""
                    )

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def langchain_model():
    model = ChatOpenAI(
        openai_api_key = api_key, 
        model = "gpt-3.5-turbo",
        temperature = 0.8, 
        max_tokens = 1000
    )
    return model

def langchain_parser():
    parser = StrOutputParser()
    return parser

def langchain_prompt():
    template = """
    Answer the question based on the context below.
    If you don't understand the question, ignore the context and just reply naturally.

    Context: {Context}

    Question: {Question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    return prompt

def langchain_retriever(concept):
    # vetordb 참조하는 부분
    #retriever = CHROMADB.as_retriever()
    retriever = ""
    retriever.invoke(concept)
    return retriever

def translate_input():
    translate_input = ChatPromptTemplate.from_template(
        "Translate {msg} to English"
    )
    return translate_input

def langchain_translate_prompt():
    translate_prompt = ChatPromptTemplate.from_template(
    "Translate {Answer} to {Language}"
    )
    return translate_prompt

#과목리스트 반환(일반 랭체인)
async def langchain_conceptlist(flag, course):
    prompt = langchain_prompt()
    model = langchain_model()
    parser = langchain_parser()
    context = contextlist[flag]

    translate = translate_input()
    message_chain = translate | model | parser
    message = message_chain.invoke({"msg":course})

    chain = prompt | model | parser

    translate_prompt = langchain_translate_prompt()
    translate_chain = (
    {"Answer": chain, "Language": itemgetter("Language")} | translate_prompt | model | parser
    )

    result = translate_chain.invoke({"Context": context, "Question": message, "Language": "Korean"})
    return result

#학습자료 생성(벡터디비 참조 랭체인)
async def langchain_learningmaterial(flag, concept):
    retriever = langchain_retriever(concept)
    setup = RunnableParallel(context = retriever, question = RunnablePassthrough())
    
    prompt = langchain_prompt()
    model = langchain_model()
    parser = langchain_parser()
    context = contextlist[flag]

    chain = setup | prompt | model | parser

    translate_prompt = langchain_translate_prompt()
    translate_chain = (
    {"Answer": chain, "Language": itemgetter("Language")} | translate_prompt | model | parser
    )
    result = translate_chain.invoke({"Context": context, "Question": concept, "Language": "Korean"})
    return result

#Q&A
async def langchain_qna(flag, question, chat):
    prompt = langchain_prompt()
    model = langchain_model()
    parser = langchain_parser()
    
    context = contextlist[flag]
    previous_chat = "\nprevious chat: " + chat
    context += previous_chat

    translate = translate_input()
    message_chain = translate | model | parser
    message = message_chain.invoke({"msg":question})

    chain = prompt | model | parser

    translate_prompt = langchain_translate_prompt()
    translate_chain = (
    {"Answer": chain, "Language": itemgetter("Language")} | translate_prompt | model | parser
    )
    result = translate_chain.invoke({"Context": context, "Question": message, "Language": "Korean"})
    return result