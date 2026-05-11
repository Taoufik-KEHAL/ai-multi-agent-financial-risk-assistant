from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_core.vectorstores import InMemoryVectorStore


# Chargement du PDF procédures
loader = PyPDFLoader(
    "data/procedures/procedures_recouvrement.pdf"
)

documents = loader.load()


# Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    add_start_index=True
)

all_splits = text_splitter.split_documents(documents)


# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Vector Store
vector_store = InMemoryVectorStore(embeddings)


# Indexation
vector_store.add_documents(documents=all_splits)


def search_procedures(query: str) -> str:
    """
    Recherche sémantique dans les procédures recouvrement.
    """

    results = vector_store.similarity_search(query, k=2)

    return "\n\n".join(
        [doc.page_content for doc in results]
    )