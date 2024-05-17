import openai
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever
import streamlit as st
import os
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableParallel

from loader import load_pdf


voorbeeld_voedingswaarden = {
    "energiebehoefte": "",
    "koolhydraten": "",
    "eiwitten": "",
    "vetten": "",
    "vezels": "",
    "ijzer": "",
    "calcium": "",
    "zink": ""
}


openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))


def generate_dietary_requirements(gender, age, height, weight, activity_level, goal):

    pdfs = load_pdf("./data/dietary_requirements")

    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore_dietary_requirements = FAISS.from_documents(
        pdfs, embeddings_model)

    llm = ChatOpenAI(openai_api_key=openai.api_key, temperature=0)
    retriever_dietary_requirements = vectorstore_dietary_requirements.as_retriever(
        search_type="similarity", search_kwargs={"k": 4})
    retriever_dietary_requirements = MultiQueryRetriever.from_llm(
        retriever=retriever_dietary_requirements, llm=llm
    )

    template = """Je bent een plantaardige voedingscoach. Beantwoord de vraag op basis van de gegeven context.
    Context: {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(documents):
        return "\n\n".join([d.page_content for d in documents])
    rag_chain_from_docs = (
        RunnablePassthrough.assign(
            context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever_dietary_requirements, "question": RunnablePassthrough(
        ), "voorbeeld_voedingswaarden": RunnablePassthrough(), "voorbeeld_maaltijdplan": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    answer = rag_chain_with_source.invoke(
        f"(Bepaal de voedingsbehoeften per dag voor een {gender} van {age} jaar, {height} cm, {weight} kilo met een {activity_level}activiteitsniveau en met als doel {goal} in json volgens het gegeven voorbeeld: {voorbeeld_voedingswaarden}")
    return answer["answer"]
