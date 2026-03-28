import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

FAISS_INDEX_PATH = "faiss_index"


def get_api_key():
    try:
        import streamlit as st
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return os.getenv("OPENAI_API_KEY")


def get_embeddings():
    return OpenAIEmbeddings(
        openai_api_key=get_api_key(),
        model="text-embedding-ada-002"
    )


def build_vector_store(policy_file: str = "data/hr_policies.txt"):
    """
    Reads HR policies, chunks them, embeds and stores in FAISS.
    """
    print("📚 Building FAISS vector store from HR policies...")

    # Read policy file
    with open(policy_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_text(text)

    # Create documents
    docs = [
        Document(page_content=chunk, metadata={"source": "hr_policies"})
        for chunk in chunks
    ]

    # Build FAISS index
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(docs, embeddings)

    # Save to disk
    vector_store.save_local(FAISS_INDEX_PATH)
    print(f"✅ FAISS index built with {len(docs)} chunks and saved!")
    return vector_store


def load_vector_store():
    """
    Loads existing FAISS index or builds a new one.
    """
    embeddings = get_embeddings()

    if os.path.exists(FAISS_INDEX_PATH):
        print("📂 Loading existing FAISS index...")
        return FAISS.load_local(
            FAISS_INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        print("🔧 No FAISS index found — building new one...")
        return build_vector_store()