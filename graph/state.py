from typing import List, NotRequired, TypedDict


class EtatAgent(TypedDict):
    question: str
    route: str
    analyse_financiere: str
    analyse_conformite: str
    niveau_risque: str
    reponse_finale: str
    brouillon_decision: NotRequired[str]
    documents: List[str]
    validation_humaine: str
    est_valide: bool
    decision_humaine: NotRequired[str]
    commentaire_humain: NotRequired[str]
    autoriser_validation_console: NotRequired[bool]
