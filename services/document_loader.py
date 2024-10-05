from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

def load_document_dir():
    """Loads documents in a directory."""

    doc_dir = "__local__"

    loader = DirectoryLoader(doc_dir, glob="*.txt")
    documents = loader.load()

    print(f">>> Loaded {len(documents)} documents from directory: {doc_dir}.")
    return documents

def split_documents_to_chunks(documents: list[Document]):
    """Splits documents into chunks."""
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)

    print(f">>> Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks