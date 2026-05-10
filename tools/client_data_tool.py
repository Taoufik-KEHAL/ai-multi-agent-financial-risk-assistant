import pandas as pd


def get_client_data(client_id: str) -> dict:
    """
    Récupère les informations financières d’un client
    depuis le fichier CSV.
    """

    csv_path = "data/clients/clients_historique.csv"

    df = pd.read_csv(csv_path)

    client = df[df["client_id"] == client_id]

    if client.empty:
        return {
            "found": False,
            "message": f"Aucun client trouvé avec l'identifiant {client_id}"
        }

    return {
        "found": True,
        "client_data": client.iloc[0].to_dict()
    }