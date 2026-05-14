import sys
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st


DOSSIER_RACINE = Path(__file__).resolve().parents[1]
if str(DOSSIER_RACINE) not in sys.path:
    sys.path.insert(0, str(DOSSIER_RACINE))

from agents.human_validation_agent import nettoyer_decision_finale, agent_validation_humaine
from graph.workflow import application


CHEMIN_CLIENTS = DOSSIER_RACINE / "data" / "clients" / "clients_historique.csv"


@st.cache_data
def charger_clients() -> pd.DataFrame:
    return pd.read_csv(CHEMIN_CLIENTS)


def construire_etat_initial(question: str) -> dict:
    return {
        "question": question,
        "route": "",
        "analyse_financiere": "",
        "analyse_conformite": "",
        "niveau_risque": "",
        "reponse_finale": "",
        "documents": [],
        "validation_humaine": "",
        "est_valide": False,
        "commentaire_humain": "",
        "autoriser_validation_console": False,
    }


def libelle_statut(resultat: dict) -> str:
    if resultat.get("est_valide"):
        return "Validée"

    message = resultat.get("validation_humaine", "")
    if "refus" in message.lower():
        return "Refusée"

    return "En attente"


def reponse_finale_pour_affichage(resultat: dict) -> str:
    reponse = nettoyer_decision_finale(
        resultat.get("brouillon_decision") or resultat.get("reponse_finale", "")
    )
    statut = libelle_statut(resultat)

    if statut == "Validée":
        resume_decision = "Décision finale : le dossier a été validé."
    elif statut == "Refusée":
        resume_decision = "Décision finale : le dossier a été refusé."
    else:
        resume_decision = "Décision finale : EN ATTENTE de validation humaine."

    reponse_finale = f"{reponse}\n\n{resume_decision}"
    commentaire = resultat.get("commentaire_humain", "").strip()

    if commentaire:
        reponse_finale += f"\nCommentaires : {commentaire}"

    return reponse_finale


def libelle_client(ligne: pd.Series) -> str:
    return f"{ligne['client_id']} - {ligne['prenom']} {ligne['nom']}"


def identifiant_client_depuis_libelle(libelle: str) -> str:
    return libelle.split(" - ", maxsplit=1)[0]


def ajouter_entree_historique(client: pd.Series, resultat: dict) -> None:
    historique = st.session_state.setdefault("historique_analyses", [])

    historique.append(
        {
            "client_id": client["client_id"],
            "client": f"{client['prenom']} {client['nom']}",
            "risque": resultat.get("niveau_risque") or client["niveau_risque"],
            "validation": libelle_statut(resultat),
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        }
    )


def mettre_a_jour_dernier_statut_historique(resultat: dict) -> None:
    historique = st.session_state.get("historique_analyses", [])

    if historique:
        historique[-1]["validation"] = libelle_statut(resultat)
        historique[-1]["risque"] = (
            resultat.get("niveau_risque") or historique[-1]["risque"]
        )


def recuperer_historique_client(identifiant_client: str) -> list[dict]:
    historique = st.session_state.get("historique_analyses", [])
    return [
        entree for entree in historique if entree["client_id"] == identifiant_client
    ]


def afficher_historique_client_selectionne(identifiant_client: str) -> str:
    historique_client = recuperer_historique_client(identifiant_client)

    if not historique_client:
        return "new"

    derniere_entree = historique_client[-1]

    st.info(
        f"Dossier déjà traité le {derniere_entree['date']} - "
        f"Risque : {derniere_entree['risque']}\n\n"
        f"Validation : {derniere_entree['validation']}."
    )

    return "history"


def main() -> None:
    st.set_page_config(
        page_title="Assistant risque financier",
        layout="wide",
    )

    clients = charger_clients()

    st.title("Assistant analyse risque financier")
    st.write("")

    with st.sidebar:
        st.header("Veuillez choisir le dossier client à analyser :")

        libelles_clients = [libelle_client(ligne) for _, ligne in clients.iterrows()]
        indice_defaut = (
            clients.index[clients["client_id"] == "C015"].tolist()[0]
            if "C015" in clients["client_id"].values
            else 0
        )

        libelle_selectionne = st.selectbox(
            "Client",
            libelles_clients,
            index=indice_defaut,
        )

        identifiant_client = identifiant_client_depuis_libelle(libelle_selectionne)
        client_selectionne = clients[
            clients["client_id"] == identifiant_client
        ].iloc[0]

        st.metric("Risque financier", client_selectionne["niveau_risque"])
        st.metric("Retard actuel", f"{client_selectionne['retard_jours']} jours")
        st.metric("Incidents", int(client_selectionne["incidents_paiement"]))

    question_defaut = (
        f"Le client {identifiant_client} peut-il obtenir une validation malgré son "
        "historique de paiement ?"
    )

    action_analyse = afficher_historique_client_selectionne(identifiant_client)

    if action_analyse == "new":
        lancer_analyse = st.button(
            "Lancer l'analyse du dossier sélectionné",
            type="primary",
        )
    else:
        lancer_analyse = action_analyse == "rerun"

    if lancer_analyse:
        with st.spinner("Analyse en cours..."):
            st.session_state["resultat_analyse"] = application.invoke(
                construire_etat_initial(question_defaut)
            )
            ajouter_entree_historique(
                client_selectionne, st.session_state["resultat_analyse"]
            )

    resultat = st.session_state.get("resultat_analyse")

    if resultat is None:
        return

    colonne_gauche, colonne_droite = st.columns([2, 1])

    with colonne_droite:
        st.metric("Validation", libelle_statut(resultat))

        if resultat.get("niveau_risque"):
            st.metric("Risque retenu", resultat["niveau_risque"].capitalize())

        st.divider()
        st.subheader("Validation de la décision finale")

        decision = st.radio(
            "Décision",
            options=["oui", "non"],
            format_func=lambda value: "Valider" if value == "oui" else "Refuser",
            horizontal=True,
        )

        commentaire = st.text_area("Commentaire", height=100)

        if st.button("Appliquer la décision", use_container_width=True):
            etat_mis_a_jour = {
                **resultat,
                "decision_humaine": decision,
                "commentaire_humain": commentaire.strip(),
                "autoriser_validation_console": False,
            }

            st.session_state["resultat_analyse"] = agent_validation_humaine(
                etat_mis_a_jour
            )
            mettre_a_jour_dernier_statut_historique(
                st.session_state["resultat_analyse"]
            )
            st.rerun()

    with colonne_gauche:
        st.subheader("Décision proposée")
        st.markdown(reponse_finale_pour_affichage(resultat))

        st.divider()

        onglet_financier, onglet_conformite = st.tabs(
            ["Analyse financière", "Conformité et procédures"]
        )

        with onglet_financier:
            st.markdown(resultat.get("analyse_financiere", ""))

        with onglet_conformite:
            st.markdown(resultat.get("analyse_conformite", ""))


if __name__ == "__main__":
    main()
