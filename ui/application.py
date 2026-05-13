import sys
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agents.human_validation_agent import human_validation_agent
from graph.workflow import app


CLIENTS_PATH = ROOT_DIR / "data" / "clients" / "clients_historique.csv"


@st.cache_data
def load_clients() -> pd.DataFrame:
    return pd.read_csv(CLIENTS_PATH)


def build_initial_state(question: str) -> dict:
    return {
        "question": question,
        "route": "",
        "financial_analysis": "",
        "conformite_analysis": "",
        "risk_level": "",
        "final_answer": "",
        "documents": [],
        "human_validation": "",
        "is_validated": False,
        "human_comment": "",
        "allow_console_validation": False,
    }


def status_label(result: dict) -> str:
    if result.get("is_validated"):
        return "Validée"

    message = result.get("human_validation", "")
    if "refusée" in message.lower():
        return "Refusée"

    return "En attente"


def client_label(row: pd.Series) -> str:
    return f"{row['client_id']} - {row['prenom']} {row['nom']}"


def client_id_from_label(label: str) -> str:
    return label.split(" - ", maxsplit=1)[0]


def main() -> None:
    st.set_page_config(
        page_title="Assistant risque financier",
        layout="wide",
    )

    clients = load_clients()

    st.title("Assistant analyse risque financier")
    st.write("")

    with st.sidebar:
        st.header("Veuillez choisir le dossier client à analyser :")

        client_labels = [client_label(row) for _, row in clients.iterrows()]
        default_index = (
            clients.index[clients["client_id"] == "C015"].tolist()[0]
            if "C015" in clients["client_id"].values
            else 0
        )

        selected_label = st.selectbox(
            "Client",
            client_labels,
            index=default_index,
        )

        client_id = client_id_from_label(selected_label)
        selected_client = clients[clients["client_id"] == client_id].iloc[0]

        st.metric("Risque financier", selected_client["niveau_risque"])
        st.metric("Retard actuel", f"{selected_client['retard_jours']} jours")
        st.metric("Incidents", int(selected_client["incidents_paiement"]))

    default_question = (
        f"Le client {client_id} peut-il obtenir une validation malgré son "
        "historique de paiement ?"
    )

    run_analysis = st.button(
        "Lancer l'analyse du dossier sélectionné",
        type="primary",
    )

    if run_analysis:
        with st.spinner("Analyse multi-agent en cours..."):
            st.session_state["analysis_result"] = app.invoke(
                build_initial_state(default_question)
            )

    result = st.session_state.get("analysis_result")

    if result is None:
        return

    left, right = st.columns([2, 1])

    with right:
        st.metric("Validation", status_label(result))

        if result.get("risk_level"):
            st.metric("Risque retenu", result["risk_level"].capitalize())

        st.divider()
        st.subheader("Validation de la décision finale")

        decision = st.radio(
            "Décision",
            options=["oui", "non"],
            format_func=lambda value: "Valider" if value == "oui" else "Refuser",
            horizontal=True,
        )

        comment = st.text_area("Commentaire", height=100)

        if st.button("Appliquer la décision", use_container_width=True):
            updated_state = {
                **result,
                "human_decision": decision,
                "human_comment": comment.strip(),
                "allow_console_validation": False,
            }

            st.session_state["analysis_result"] = human_validation_agent(updated_state)
            st.rerun()

    with left:
        st.subheader("Décision proposée")
        st.markdown(result.get("final_answer", ""))

        st.divider()

        tab_financial, tab_conformite = st.tabs(
            ["Analyse financière", "Conformité et procédures"]
        )

        with tab_financial:
            st.markdown(result.get("financial_analysis", ""))

        with tab_conformite:
            st.markdown(result.get("conformite_analysis", ""))


if __name__ == "__main__":
    main()
