from tools.rag_vectorstore import search_pdf_context


PROCEDURES_PDF_PATH = "data/procedures/procedures_recouvrement.pdf"
PROCEDURES_VECTORSTORE_PATH = "vectorstores/procedures/store.json"


def search_procedures(query: str) -> str:
    """
    Recherche sémantique dans les procédures recouvrement.
    """

    return search_pdf_context(
        pdf_path=PROCEDURES_PDF_PATH,
        store_path=PROCEDURES_VECTORSTORE_PATH,
        query=query,
        k=2,
    )
