# Assistant Analyse Risque Financier

Assistant multi-agent pour l'analyse du risque financier d'un dossier client. Le projet combine un workflow LangGraph, des agents spécialisés, des données clients CSV, un RAG documentaire sur des PDF internes, des appels LLM via Groq et une interface Streamlit.

## Objectif

L'application permet d'analyser un dossier client à partir de données financières et de règles internes afin de produire une recommandation argumentée :

- analyse financière du client ;
- analyse conformité et procédures de recouvrement ;
- évaluation finale du niveau de risque ;
- validation humaine de la décision finale.

## Fonctionnalités

- Workflow multi-agent avec LangGraph.
- Agent financier connecté au CSV clients.
- RAG séparé pour les règles de conformité et les procédures de recouvrement.
- Vectorstores persistants dans `vectorstores/`.
- Appels LLM avec Groq.
- Human-in-the-loop compatible terminal et Streamlit.
- Interface Streamlit pour lancer une analyse et valider la décision.

## Architecture

```text
.
├── agents/              # Agents du workflow
├── config/              # Configuration LLM
├── data/                # Sources de données
│   ├── clients/         # CSV clients
│   ├── conformite/      # PDF règles conformité
│   └── procedures/      # PDF procédures recouvrement
├── graph/               # Etat partagé et workflow LangGraph
├── prompts/             # Prompts utilisés par les agents
├── tools/               # Tools CSV, RAG, validation humaine
├── ui/                  # Interface Streamlit
├── vectorstores/        # Index RAG persistants
├── main.py              # Exécution terminal
└── pyproject.toml       # Dépendances uv
```

## Workflow

Le workflow suit les étapes suivantes :

1. `supervisor` : initialise le routage de la demande.
2. `financial` : récupère les données CSV du client et génère l'analyse financière.
3. `conformite` : interroge les documents PDF via RAG et produit l'analyse conformité.
4. `evaluator` : combine les analyses et produit la décision finale.
5. `human_validation` : applique une validation humaine ou laisse la décision en attente.

## Installation

Le projet utilise `uv`.

```bash
uv sync
```

Créer ensuite un fichier `.env` à la racine du projet :

```env
GROQ_API_KEY=your_groq_api_key
```

## Lancement en terminal

```bash
uv run python main.py
```

Le script lance le workflow sur un exemple de dossier client et demande une validation humaine dans le terminal.

## Lancement de l'interface Streamlit

```bash
uv run streamlit run ui/app.py
```

L'interface permet de :

- sélectionner un dossier client ;
- lancer l'analyse ;
- consulter la décision proposée ;
- afficher les analyses financière et conformité ;
- valider ou refuser la décision finale.

## Données utilisées

- `data/clients/clients_historique.csv` : historique clients et indicateurs financiers.
- `data/conformite/regles_conformite.pdf` : règles internes de validation et conformité.
- `data/procedures/procedures_recouvrement.pdf` : procédures internes de recouvrement.

## RAG documentaire

Deux retrievers séparés sont utilisés :

- `tools/conformite_retriever.py` pour les règles de conformité ;
- `tools/procedure_retriever.py` pour les procédures de recouvrement.

La logique commune de chargement PDF, chunking, embeddings et persistance se trouve dans `tools/rag_vectorstore.py`.

Les vectorstores sont persistés dans :

- `vectorstores/conformite/store.json`
- `vectorstores/procedures/store.json`

Au premier lancement sur une nouvelle machine, le modèle d'embeddings HuggingFace peut nécessiter un accès réseau pour être téléchargé.

## Tests

Si les tests sont présents dans le dossier local `tests/`, ils peuvent être lancés avec :

```bash
uv run pytest
```

La suite couvre notamment le CSV tool, le chargement des prompts, la validation humaine, certains helpers RAG et l'interface.

## Technologies

- Python
- uv
- LangGraph
- LangChain
- Groq
- HuggingFace embeddings
- Streamlit
- pandas
- PyPDF

## Limites

- Les décisions générées restent une aide à l'analyse et nécessitent une validation humaine.
- Le RAG dépend de la qualité et de la couverture des documents PDF fournis.
- Le modèle d'embeddings doit être disponible localement ou téléchargeable au premier usage.
- Les résultats LLM peuvent varier selon le modèle et les prompts.
