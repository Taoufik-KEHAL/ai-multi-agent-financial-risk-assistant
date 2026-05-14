import pandas as pd


def recuperer_donnees_client(identifiant_client: str) -> dict:
    """
    Récupère les informations financières d’un client
    depuis le fichier CSV.
    """

    chemin_csv = "data/clients/clients_historique.csv"

    donnees_clients = pd.read_csv(chemin_csv)

    client = donnees_clients[donnees_clients["client_id"] == identifiant_client]

    if client.empty:
        return {
            "trouve": False,
            "message": f"Aucun client trouvé avec l'identifiant {identifiant_client}"
        }

    return {
        "trouve": True,
        "donnees_client": client.iloc[0].to_dict()
    }
