import streamlit as st
import os
import openai

from openai import OpenAI
import os
from openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader, DataFrameLoader
import pandas as pd
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma, FAISS, LanceDB
from langchain_openai import ChatOpenAI
from langchain_core.runnables import (
    RunnableParallel,
    RunnableLambda,
    RunnablePassthrough
)
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo


openai.api_key = os.getenv(st.secrets["OPENAI_API_KEY"])


st.title("Vegan maaltijdplangenerator")


def generate_meal_plan(gender= 'vrouw', age = 34, height = 163, weight = 75, activity_level = 'gemiddeld', goal = '0.5 kilo per week afvallen'):
    try:
        user_template = f"Stel een plantaardig dagelijks maaltijdplan op dat voldoet aan de voedingsbehoeften van een {gender} van {age} jaar, {weight} kilo, {height} cm, met een {activity_level} activiteitsniveau en als doel {goal}. De totale voedingswaarden stemmen overeen met de voedingsbehoeften. Het plan is gedetailleerd en bevat minstens ontbijt, lunch, snacks en diner en eventueel dessert."

        completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "Je bent een voedingscoach die plantaardige maaltijdplannen opstelt."},
        {"role": "user", "content": user_template}
    ]
)
        

        

   

        return completion.choices[0].message.content.replace('\\n', '\n')

    except Exception as e:
        return f"Een fout is opgetreden: {str(e)}"

gender = st.selectbox('Geslacht', ['Man', 'Vrouw', 'Non-binair persoon'])
age = st.number_input('Leeftijd', min_value=1, max_value=100, value=30, step=1)
height = st.number_input('Lengte (cm)', min_value=1,
                         max_value=220, value=170, step=1)
weight = st.number_input('Gewicht (kg)', min_value=1,
                         max_value=500, value=70, step=1)
activity_level = st.selectbox('Activiteitsniveau', [
                              'Sedentair', 'Licht actief', 'Gemiddeld actief', 'Zeer actief'])
goal = st.selectbox('Doel', ['0.5 kilo per week aankomen', '1 kilo per week aankomen',
                    '0.5 kilo per week afvallen', '1 kilo per week afvallen', 'Onderhouden'])

# Knop om maaltijdplan te genereren
if st.button('Genereer Maaltijdplan'):
    # Genereer maaltijdplan op basis van gebruikersinvoer
    st.header('Jouw Maaltijdplan')
    st.write(generate_meal_plan(
        gender, age, height, weight, activity_level, goal))

   




import random
def generate_motivation():
     
    onderwerpen = [
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

    willekeurig_onderwerp = random.choice(onderwerpen)



    #RAG
    #Data
    files_paths = []
    files_paths.append('/RAG_motivatie/vegan_diet2.pdf')
    files_paths.append('/RAG_motivatie/sustainability.pdf')

    #Document loader
    documents_motivatie = []
    for pdf_path in files_paths:
            loader = PyPDFLoader(pdf_path)
            documents_motivatie.extend(loader.load())


    #Text Splitter
    documents_benefits = loader.load_and_split()

    #Embeddings
    embeddings_model = OpenAIEmbeddings(api_key= openai.api_key)
    # Vectorstores
    vectorstore_motivatie = LanceDB.from_documents(documents_motivatie, embeddings_model)



    llm = ChatOpenAI(openai_api_key= openai.api_key, temperature=0)
    retriever_motivatie = vectorstore_motivatie.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=retriever_motivatie, llm=llm
)


    template = """Je bent een plantaardige voedingscoach. Beantwoord de vraag enkel op basis van de volgende context:

    vraag: {question}
    context: {context}
    """
    prompt = ChatPromptTemplate.from_template(template)



    def format_docs(documents):
        return "\n\n".join([d.page_content for d in documents])


    from langchain_core.runnables import RunnableParallel

    rag_chain_from_pages = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        |  prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever_motivatie, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_pages)
    antwoord = rag_chain_with_source.invoke(f"Schrijf een hippe, inspirerende en creatieve aanmoediging of tip op basis van één concreet voordeel, ondersteund door middel van concrete statistieken en cijfers uit de gegeven bronnen, van een plantaardig dieet op vlak van {willekeurig_onderwerp} in maximum een of twee zinnen")

    return antwoord['answer']


st.sidebar.markdown(generate_motivation())
st.write(generate_motivation())