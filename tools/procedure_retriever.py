from tools.rag_vectorstore import rechercher_contexte_pdf


CHEMIN_PDF_PROCEDURES = "data/procedures/procedures_recouvrement.pdf"
CHEMIN_VECTORSTORE_PROCEDURES = "vectorstores/procedures/store.json"


def rechercher_procedures(requete: str) -> str:
    """
    Recherche sémantique dans les procédures recouvrement.
    """

    return rechercher_contexte_pdf(
        chemin_pdf=CHEMIN_PDF_PROCEDURES,
        chemin_store=CHEMIN_VECTORSTORE_PROCEDURES,
        requete=requete,
        nombre_resultats=2,
    )
