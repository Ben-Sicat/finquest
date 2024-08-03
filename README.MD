### RAG System with Flask and Langchain
This project implements a RAG system for financial advice. It utilizes Flask to build a REST API and leverages LangChain for generating embeddings.

## Functionalities 
- Users interact with the system through the REST API or the app built with unity (FINQUEST)
- User data is processed and potentially pre-processed for model compatibility.
- LangChain generates an embedding representation of the user data.
- Pre-defined prompts are adapted to incorporate the user embedding reference.
- The LLM API receives the adapted prompt and generates financial advice.
- The generated financial advice is returned as a JSON response through the API.

## Getting Started

1. *Installation*: Create a venv and activate it. Install all reqruired libraries and dependedcies through `pip install -r requirements.txt` 
2. *Configuration*: Replace placeholder values in `config.py` with actual configuration details 
3. *Running the system*: Run the Flask App using python flask_app/app.py to start the API server.

## Further Development:

This project provides a foundation for building a more elaborate RAG system. You can expand it by:

- Implementing a user interface layer.
- Integrating custom LLM API interaction scripts.
- Connecting to an external database for user data storage.

## Authors:
Benito Raphael T. Sicat IV
