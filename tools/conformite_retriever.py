from tools.rag_vectorstore import rechercher_contexte_pdf


CHEMIN_PDF_CONFORMITE = "data/conformite/regles_conformite.pdf"
CHEMIN_VECTORSTORE_CONFORMITE = "vectorstores/conformite/store.json"


def rechercher_conformite(requete: str) -> str:
    """
    Recherche sémantique dans les règles de conformité.
    """

    return rechercher_contexte_pdf(
        chemin_pdf=CHEMIN_PDF_CONFORMITE,
        chemin_store=CHEMIN_VECTORSTORE_CONFORMITE,
        requete=requete,
        nombre_resultats=2,
    )
