import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI

client = OpenAI()

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="pdf_docs")


def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_text(text)


def store_embeddings(text, doc_id):
    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"{doc_id}_{i}"]
        )


def search_context(query):
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    return results["documents"][0] if results["documents"] else []