from tools.rag_vectorstore import search_pdf_context


CONFORMITE_PDF_PATH = "data/conformite/regles_conformite.pdf"
CONFORMITE_VECTORSTORE_PATH = "vectorstores/conformite/store.json"


def search_conformite(query: str) -> str:
    """
    Recherche sémantique dans les règles de conformité.
    """

    return search_pdf_context(
        pdf_path=CONFORMITE_PDF_PATH,
        store_path=CONFORMITE_VECTORSTORE_PATH,
        query=query,
        k=2,
    )
