from functools import lru_cache
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    try:
        return HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"local_files_only": True},
        )
    except Exception:
        return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def load_or_create_vectorstore(pdf_path: str, store_path: str) -> InMemoryVectorStore:
    """
    Charge un vector store persistant s'il est à jour, sinon le reconstruit
    depuis le PDF source.
    """

    pdf = Path(pdf_path)
    store = Path(store_path)

    if not pdf.exists():
        raise FileNotFoundError(f"PDF introuvable : {pdf}")

    embeddings = get_embeddings()

    if _is_store_current(store, pdf):
        return InMemoryVectorStore.load(str(store), embedding=embeddings)

    documents = PyPDFLoader(str(pdf)).load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True,
    )

    splits = text_splitter.split_documents(documents)
    vector_store = InMemoryVectorStore(embeddings)
    vector_store.add_documents(documents=splits)
    vector_store.dump(str(store))

    return vector_store


def search_pdf_context(pdf_path: str, store_path: str, query: str, k: int = 2) -> str:
    vector_store = load_or_create_vectorstore(pdf_path, store_path)
    results = vector_store.similarity_search(query, k=k)

    return "\n\n".join(doc.page_content for doc in results)


def _is_store_current(store: Path, pdf: Path) -> bool:
    return store.exists() and store.stat().st_mtime >= pdf.stat().st_mtime
