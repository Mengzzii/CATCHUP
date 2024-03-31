import os
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from operator import itemgetter

from langchain_community.document_loaders import TextLoader
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

contextlist = []
#기본챗방에서 개념리스트 반환용 프롬프트 엔지니어링
# contextlist[0]
contextlist.append("""You are a Computer science professor.
                    If the student gives the course name, then you have to give an essential prerequisites concept list that is required to take that course. 
                    Each concept should be narrowed enough to be covered within 30 minutes.
                    Guidelines to formatting:
                    - format: JSON
                    - No code block delimiter.
                    - Contain the key "concepts" and then place the concepts in a List format.
                    - example: {"concepts": [{"name": "concept1"}, {"name": "concept2"},{"name": "concept3"}, ...]"""
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

def langchain_model():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    model = ChatOpenAI(
        openai_api_key=api_key, 
        model="gpt-3.5-turbo",
        temperature=1.00, 
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return model

def langchain_parser():
    parser = StrOutputParser()
    return parser

def langchain_prompt():
    template = """
    Answer the question based on the context below.
    If you can't answer the question, reply "I don't know".

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

    chain = prompt | model | parser

    translate_prompt = langchain_translate_prompt()
    translate_chain = (
    {"Answer": chain, "Language": itemgetter("Language")} | translate_prompt | model | parser
    )

    result = translate_chain.invoke({"Context": context, "Question": course, "Language": "Korean"})
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

    chain = prompt | model | parser

    translate_prompt = langchain_translate_prompt()
    translate_chain = (
    {"Answer": chain, "Language": itemgetter("Language")} | translate_prompt | model | parser
    )
    result = translate_chain.invoke({"Context": context, "Question": question, "Language": "Korean"})
    return result