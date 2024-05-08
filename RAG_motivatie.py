
import random
import openai
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import LanceDB
from langchain_openai import ChatOpenAI
from langchain_core.runnables import (
   # RunnableParallel,
   # RunnableLambda,
    RunnablePassthrough
)
from langchain_core.output_parsers import StrOutputParser
#from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever
#from langchain.chains.query_constructor.base import AttributeInfo
from loader import load_pdf

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
    


    #Text Splitter
    documents_motivatie = load_pdf().load_and_split()

    #Embeddings
    embeddings_model = OpenAIEmbeddings(api_key= openai.api_key)
    # Vectorstores
    vectorstore_motivatie = LanceDB.from_documents(documents_motivatie, embeddings_model)



    llm = ChatOpenAI(openai_api_key= openai.api_key, temperature=0)
    retriever_motivatie = vectorstore_motivatie.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    retriever_motivatie= MultiQueryRetriever.from_llm(
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