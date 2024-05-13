
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader 
from langchain_community.document_loaders import DataFrameLoader

def list_pdf(data_dir="./data/motivation"):
    paths = Path(data_dir).glob('**/*.pdf')
    for path in paths:
        yield str(path)


def load_pdf(data_dir="./data/motivation"):
    pdfs = []
    paths = list_pdf(data_dir)
    for path in paths:
        print(f"Loading {path}")
        loader = PyPDFLoader(path)
        pdfs.extend(loader.load_and_split())
    return pdfs

