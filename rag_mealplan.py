from langchain_community.document_loaders import DataFrameLoader
import pandas as pd
import openai
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
import streamlit as st
import os
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableParallel
from pathlib import Path


# voorbeelden
voorbeeld_voedingswaarden2 = {
  "energiebehoefte": 1947,
  "koolhydraten": "219-274 gram",
  "eiwitten": "94-119 gram",
  "vetten": "63-78 gram",
  "vezels": "minimaal 25 gram",
  "ijzer": "18 mg",
  "calcium": "1000 mg",
  "zink": "8 mg"
}

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

voorbeeld_maaltijdplan = {
    "maaltijdplan": {
        "ontbijt": {
            "gerecht": "Vegan avocado toast",
            "moeilijkheidsgraad": "Gemakkelijk",
            "kooktijd": "10 minuten",
            "benodigdheden": {
                "oven": 1,
                "broodrooster": 1
            },
            "ingrediënten": {
                "avocado": "1",
                "volkorenbrood": "2 sneetjes",
                "citroensap": "1 eetlepel",
                "chilivlokken": "naar smaak",
                "zout en peper": "naar smaak"
            },
            "bereidingswijze": "1. Rooster het volkorenbrood in de broodrooster.\n2. Prak de avocado en besprenkel met citroensap.\n3. Besmeer het geroosterde brood met de geprakte avocado.\n4. Breng op smaak met chilivlokken, zout en peper naar smaak."
        },
        "lunch": {
            "gerecht": "Quinoa bowl met geroosterde groenten",
            "moeilijkheidsgraad": "Gemiddeld",
            "kooktijd": "30 minuten",
            "benodigdheden": {
                "oven": 1,
                "kookpan": 1
            },
            "ingrediënten": {
                "quinoa": "1 kopje gekookt",
                "paprika": "1, in stukken",
                "courgette": "1, in plakjes",
                "cherrytomaten": "1 kopje, gehalveerd",
                "olijfolie": "2 eetlepels",
                "verse kruiden (bijv. basilicum en peterselie)": "naar smaak",
                "citroensap": "1 eetlepel",
                "zout en peper": "naar smaak"
            },
            "bereidingswijze": "1. Verwarm de oven voor op 200°C.\n2. Meng de gesneden paprika, courgette en cherrytomaten met olijfolie, zout en peper.\n3. Rooster de groenten in de voorverwarmde oven gedurende 20-25 minuten, tot ze gaar zijn.\n4. Kook de quinoa volgens de aanwijzingen op de verpakking.\n5. Meng de gekookte quinoa met de geroosterde groenten.\n6. Besprenkel met citroensap en garneer met verse kruiden."
        },
        "diner": {
            "gerecht": "Cauliflower 'steak' met romesco saus",
            "moeilijkheidsgraad": "Uitdagend",
            "kooktijd": "45 minuten",
            "benodigdheden": {
                "oven": 1,
                "grillpan": 1
            },
            "ingrediënten": {
                "bloemkool": "1 grote, in plakken",
                "olijfolie": "2 eetlepels",
                "amandelen": "½ kopje",
                "geroosterde rode paprika (uit pot)": "½ kopje",
                "knoflook": "2 teentjes",
                "citroensap": "1 eetlepel",
                "gerookt paprikapoeder": "1 theelepel",
                "zout en peper": "naar smaak"
            },
            "bereidingswijze": "1. Verwarm de oven voor op 200°C.\n2. Snijd de bloemkool in plakken van ongeveer 1 cm dik.\n3. Meng olijfolie, knoflook, gerookt paprikapoeder, zout en peper en bestrijk de bloemkoolplakken aan beide zijden met dit mengsel.\n4. Bak de bloemkoolplakken in een grillpan tot ze aan beide kanten goudbruin zijn.\n5. Plaats de gebakken bloemkoolplakken op een bakplaat en rooster ze gedurende 25-30 minuten in de voorverwarmde oven, tot ze zacht zijn.\n6. Maak ondertussen de romesco saus door amandelen, geroosterde rode paprika, knoflook, citroensap, zout en peper in een blender te mengen tot een gladde saus.\n7. Serveer de geroosterde bloemkoolplakken met de romesco saus."
        },
        "dessert": {
            "gerecht": "Chocolade avocado mousse",
            "moeilijkheidsgraad": "Gemakkelijk",
            "kooktijd": "10 minuten",
            "benodigdheden": {
                "blender": 1,
                "koelkast": 1
            },
            "ingrediënten": {
                "avocado": "1",
                "cacao poeder": "2 eetlepels",
                "agave siroop": "2 eetlepels",
                "vanille extract": "1 theelepel",
                "plantaardige melk": "¼ kopje",
                "zout": "een snufje"
            },
            "bereidingswijze": "1. Schep het vruchtvlees van de avocado in een blender.\n2. Voeg cacao poeder, agave siroop, vanille extract, plantaardige melk en een snufje zout toe.\n3. Blend tot een gladde mousse.\n4. Zet de mousse minstens een uur in de koelkast om op te stijven.\n5. Serveer gekoeld."
        },
        "snack": {
            "gerecht": "Geroosterde kikkererwten",
            "moeilijkheidsgraad": "Gemakkelijk",
            "kooktijd": "40 minuten",
            "benodigdheden": {
                "oven": 1,
                "bakplaat": 1
            },
            "ingrediënten": {
                "kikkererwten (uit blik, uitgelekt en afgespoeld)": "1 blikje",
                "olijfolie": "1 eetlepel",
                "paprikapoeder": "1 theelepel",
                "komijnpoeder": "1 theelepel",
                "knoflookpoeder": "½ theelepel",
                "zout en peper": "naar smaak"
            },
            "bereidingswijze": "1. Verwarm de oven voor op 200°C.\n2. Dep de kikkererwten droog met keukenpapier en verwijder eventuele losse velletjes.\n3. Meng de kikkererwten met olijfolie, paprikapoeder, komijnpoeder, knoflookpoeder, zout en peper.\n4. Verdeel de gekruide kikkererwten over een met bakpapier beklede bakplaat.\n5. Rooster de kikkererwten in de voorverwarmde oven gedurende 30-35 minuten, schud ze halverwege de baktijd om, tot ze knapperig en goudbruin zijn.\n6. Laat de geroosterde kikkererwten afkoelen voordat je ze serveert."
        }
    },
    "totaal_voedingswaarden": {
        "calorieën": "1510 kcal",
        "koolhydraten": "125g",
        "vetten": "79g",
        "eiwitten": "41g",
        "vezels": "36g",
        "ijzer": "10.3mg",
        "calcium": "150mg",
        "zink": "6.6mg"
    }
}

openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))

def generate_mealplan():

    df = pd.DataFrame()
    paths = Path("./data/recipes").glob('**/*.csv')
    for path in paths:
        temp_df = pd.read_csv(filepath_or_buffer=str(path))
        temp_df = temp_df.rename(columns={'Unnamed: 0': 'id'})
    df = pd.concat([df, temp_df], ignore_index=True)
        
    
    #Document loader
    loader = DataFrameLoader(df, page_content_column="ingredients")
    recipes = loader.load()

    #Embeddings
    embeddings_model = OpenAIEmbeddings(model = "text-embedding-3-small")

    # Vectorstores
    vectorstore_mealplan = FAISS.from_documents(recipes, embeddings_model)
    import random
    def random_num():
        id_list = []
        for i in range(8):
            id_list.append(random.randint(0, 1389))
        return str(id_list)

    metadata_field_info = [
        AttributeInfo(
            name="id",
            description="nummer",
            type="integer",
        ),


        AttributeInfo(
            name="title",
            description="Title of recepy",
            type="string",
        ),


        ]
    document_content_description = "Vegan recepies"
    llm = ChatOpenAI(openai_api_key= openai.api_key, model="gpt-3.5-turbo", response_format = {"type": "json_object" })
    retriever_maaltijdplan = SelfQueryRetriever.from_llm(
        llm,
        vectorstore_mealplan,
        document_content_description,
        metadata_field_info,
        verbose = True,
        search_type='similarity',
        search_kwargs={'k': 10}
    )



    template = """Je bent een plantaardige voedingscoach die plantaardige maaltijdplannen opstelt in het Nederlands op basis van de gegeven context. Stel een dagelijks plantaardig maaltijdplan op in json met dezelfde structuur als in het gegeven voorbeeld. De totale voedingswaarden van de gerechten moeten exact overeenkomen met de gegeven voedingsbehoeften.
    Voorbeeld: {voorbeeld_maaltijdplan}
    Context: {context}
    Voedingsbehoeften: {voedingswaarden}             
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)



    def format_docs(documents):
        return "\n\n".join([d.page_content for d in documents])
    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
    {"context": retriever_maaltijdplan, "question": RunnablePassthrough(), "voorbeeld_voedingswaarden" :RunnablePassthrough(), "voorbeeld_maaltijdplan": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)
    answer2 = rag_chain_with_source.invoke(f" id, {random_num()}")
    answer = rag_chain_with_source.invoke(f"(Gebruik acai als ingrediënt voor het onbijt, hummus als snack, seitan voor de lunch en rijstpap als dessert en tomaat voor het diner.  {voorbeeld_maaltijdplan}, {voorbeeld_voedingswaarden}")
    return answer["answer"]

generate_mealplan()