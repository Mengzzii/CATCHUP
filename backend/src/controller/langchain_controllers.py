import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from operator import itemgetter
from ..db.chromadb import (chromadb_main)
from langchain_community.document_loaders import TextLoader
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# 프롬프트 엔지니어링 context 저장 배열
contextlist = []
# 기본챗방에서 개념리스트 반환용 프롬프트 엔지니어링
# contextlist[0]
contextlist.append("""You are computer science professor.
                   I'm trying to develop a chatbot to assist struggling computer science students.
                   When a user specifies a subject for study, you should supply a concise yet comprehensive list of relevant concepts to take that course. 
                   It is crucial that when presenting these concepts, they are meticulously broken down into detailed units. 
                   For instance, instead of just giving the broad terms, each concept must be separately stated.
                   Additionally, we want to store the provided list into MongoDB using a model called Concept, which includes the fields "name: str" . 
                   So please print out the result in json format to facilitate entering this model.
                      - format: List of JSON
                      - No code block delimiter.
                      - Do not add other comments, only return the list of JSON.
                      - example : [{"name":"concept1"}, {"name":"concept2"},{"name":"concept3"}, ...]"""
                   )
# 학습자료 제공용 프롬프트 엔지니어링
# contextlist[1]
contextlist.append("""You are a Computer science professor.
                    You will make learning resources for your freshman university student. 
                    I'm going to give you the context, concept, and material you can refer to.
                    You should make the learning resources based on context,  concept, and material.
                    Learning resources should contain enough content to fully understand that specific concept and the amount of content should be made so that the learning can be completed in 1 hour. 
                    So, explain the contents in as much detail as possible in expert-level writing with various examples related to the concept that can help students more easily understand.
                    """
                    )
# 개념챗방에서 Q&A용 프롬프트 엔지니어링
# contextlist[2]
contextlist.append("""You are a Computer science professor.
                    Please answer the question in as much detail as possible and kindly as possible
                    And please answer the question in context based on the previous chat that is given.
                    Also, sympathize with the student!"""
                    )

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# gpt model
# open api gpt 모델 불러옴
def langchain_model():
    model = ChatOpenAI(
        openai_api_key = api_key, 
        model = "gpt-3.5-turbo",
        temperature = 1.0, 
        max_tokens = 4096
    )
    return model

# parser
# 내용만 가져오도록 함
def langchain_parser():
    parser = StrOutputParser()
    return parser

# prompt
# 프롬프트 엔지니어링
def langchain_prompt():
    template = """
    Answer the Question based on the context, PreviousChat, Material.
    Context is the mandatory field but others are not.  So, If the prviousChat or Material is empty, ignore that specific field.
    And Answer the Question as detailed as possible in expert-level.
    If you don't understand the Question, ignore the context and just reply naturally.

    Context: {Context}

    Question: {Question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    return prompt

# retriever
# vector db 참조
def langchain_retriever(concept):
    retriever = chromadb_main(concept)
    return retriever

# 사용자 입력을 영어로 변환
def translate_input():
    translate_input = ChatPromptTemplate.from_template(
        "Translate {msg} to English"
    )
    return translate_input

# gpt 답변을 지정 언어로 변환
def langchain_translate_prompt():
    translate_prompt = ChatPromptTemplate.from_template(
    "Translate {Answer} to {Language}"
    )
    return translate_prompt


# 개념 리스트 반환
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

# 학습자료 생성(벡터디비 참조 랭체인)
async def langchain_learningmaterial(flag, concept):
    material = chromadb_main(concept)
    prompt = langchain_prompt()
    model = langchain_model()
    parser = langchain_parser()
    context = contextlist[flag]+"\n[concept]\n"+concept+"\n[material]\n"+material
    chain = prompt | model | parser

    translate_prompt = langchain_translate_prompt()
    translate_chain = (
    {"Answer": chain, "Language": itemgetter("Language")} | translate_prompt | model | parser
    )
    result = translate_chain.invoke({"Context": context, "Question": concept, "Language": "Korean"})
    return result

# Q&A
async def langchain_qna(flag, question, chat):
    prompt = langchain_prompt()
    model = langchain_model()
    parser = langchain_parser()
    
    context = contextlist[flag]+"\n[Previous Chat]\n"+chat

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