from functools import lru_cache
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


MODELE_EMBEDDING = "sentence-transformers/all-MiniLM-L6-v2"
TAILLE_FRAGMENT = 300
CHEVAUCHEMENT_FRAGMENT = 50


@lru_cache(maxsize=1)
def obtenir_embeddings() -> HuggingFaceEmbeddings:
    try:
        return HuggingFaceEmbeddings(
            model_name=MODELE_EMBEDDING,
            model_kwargs={"local_files_only": True},
        )
    except Exception:
        return HuggingFaceEmbeddings(model_name=MODELE_EMBEDDING)


def charger_ou_creer_vectorstore(
    chemin_pdf: str, chemin_store: str
) -> InMemoryVectorStore:
    """
    Charge un vector store persistant s'il est à jour, sinon le reconstruit
    depuis le PDF source.
    """

    pdf = Path(chemin_pdf)
    chemin_vectorstore = Path(chemin_store)

    if not pdf.exists():
        raise FileNotFoundError(f"PDF introuvable : {pdf}")

    embeddings = obtenir_embeddings()

    if _store_est_a_jour(chemin_vectorstore, pdf):
        return InMemoryVectorStore.load(str(chemin_vectorstore), embedding=embeddings)

    documents = PyPDFLoader(str(pdf)).load()

    decoupeur_texte = RecursiveCharacterTextSplitter(
        chunk_size=TAILLE_FRAGMENT,
        chunk_overlap=CHEVAUCHEMENT_FRAGMENT,
        add_start_index=True,
    )

    fragments = decoupeur_texte.split_documents(documents)
    vectorstore = InMemoryVectorStore(embeddings)
    vectorstore.add_documents(documents=fragments)
    vectorstore.dump(str(chemin_vectorstore))

    return vectorstore


def rechercher_contexte_pdf(
    chemin_pdf: str, chemin_store: str, requete: str, nombre_resultats: int = 2
) -> str:
    vectorstore = charger_ou_creer_vectorstore(chemin_pdf, chemin_store)
    resultats = vectorstore.similarity_search(requete, k=nombre_resultats)

    return "\n\n".join(document.page_content for document in resultats)


def _store_est_a_jour(chemin_store: Path, chemin_pdf: Path) -> bool:
    return (
        chemin_store.exists()
        and chemin_store.stat().st_mtime >= chemin_pdf.stat().st_mtime
    )
