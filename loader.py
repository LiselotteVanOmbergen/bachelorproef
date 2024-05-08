


from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader 





#from langchain.retrievers.self_query.base import SelfQueryRetriever

#from langchain.chains.query_constructor.base import AttributeInfo

def list_pdf(data_dir="./data/motivatie"):
    paths = Path(data_dir).glob('**/*.pdf')
    for path in paths:
        yield str(path)


def load_pdf(data_dir="./data/motivatie"):
    pdfs = []
    paths = list_pdf(data_dir)
    for path in paths:
        print(f"Loading {path}")
        loader = PyPDFLoader(path)
        pdfs.extend(loader.load())
    return pdfs

