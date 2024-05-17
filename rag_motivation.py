
import random
import openai
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import LanceDB
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever
import streamlit as st
import os
from loader import load_pdf

openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))


def generate_motivation():

    subjects = [
        "Gezondheid",
        "Milieubewustzijn",
        "Dierenwelzijn",
        "Duurzaamheid",
        "Gewichtsbeheersing",
        "Ethiek",
        "Voedseldiversiteit",
        "Klimaatverandering",
        "Economische rechtvaardigheid"
    ]

    random_subject = random.choice(subjects)

    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

    pdfs = load_pdf("./data/motivation")
    vectorstore_motivatie = LanceDB.from_documents(pdfs, embeddings_model)

    llm = ChatOpenAI(openai_api_key=openai.api_key, temperature=0)
    retriever_motivation = vectorstore_motivatie.as_retriever(
        search_type="similarity", search_kwargs={"k": 4})
    retriever_motivation = MultiQueryRetriever.from_llm(
        retriever=retriever_motivation, llm=llm
    )

    template = """Je bent een Nederlandstalige plantaardige voedingscoach. Beantwoord de vraag uitsluitend in het Nederlands enkel op basis van de volgende context:

    vraag: {question}
    context: {context}
    """
    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(documents):
        return "\n\n".join([d.page_content for d in documents])

    from langchain_core.runnables import RunnableParallel

    rag_chain_from_pages = (
        RunnablePassthrough.assign(
            context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever_motivation, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_pages)
    output = rag_chain_with_source.invoke(
        f"Schrijf een hippe, inspirerende en creatieve aanmoediging of tip in het Nederlands op basis van één concreet voordeel, ondersteund door middel van concrete statistieken en cijfers uit de gegeven bronnen, van een plantaardig dieet op vlak van {random_subject} in maximum één of twee zinnen")

    return output['answer']
