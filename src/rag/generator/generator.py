import asyncio
import os
from typing import List

from dotenv import load_dotenv
from langchain.schema import Document
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_google_vertexai import (ChatVertexAI, VertexAIEmbeddings)
from src.db.CRUD.document_crud import DocumentCRUD
from langchain.schema.runnable import RunnableMap
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from motor.motor_asyncio import AsyncIOMotorClient  # Import AsyncIOMotorClient
import logging
output_parser = StrOutputParser()

load_dotenv()

DB_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = "documents"
CONNECTION_STRING = os.getenv('MONGO_URL')
# Initialize Vertex AI Embeddings
embeddings = VertexAIEmbeddings(
    model="text-embedding-004", project="finquest", location="us-central1"
)

async def fetch_all_documents() -> List[Document]:
    """Fetches all documents from the specified MongoDB collection."""
    #use DocumentCRUD to get all documents
    documents = await DocumentCRUD.get_all_documents_content()
    content_list = [doc['content'] for doc in documents]
    logging.info(f"Fetched {len(content_list)} documents.")
    return content_list
async def initialize_db():
    # Fetch documents directly
    docs = await fetch_all_documents()

    # Extract content from documents and embed them
    db = DocArrayInMemorySearch.from_texts(
         docs, embeddings
    )
    return db

# Initialize Vertex AI Chat Model
gemini = ChatVertexAI(
    model="gemini-1.5-flash-001", project="finquest", location="us-central1",max_output_tokens=1500
)

# Create retriever (outside the async function as it depends on the awaited db)
async def main():
    db = await initialize_db()
    retriever = db.as_retriever(
        search_type="similarity", search_kwargs={"score_threshold": 0.4, "k": 3}
    )
    # Define prompt template
    template = """Use the following context to answer the question. 
    Act as if you were a financial advisor. and elaborate on your suggestions why I should do your suggestions. 
    Your goal is to help me be financially literate, so teach me how to:
    1. allocate, budget and prioritize income based on the needs of a typical filipino person.
    2. identify non essentials in my expenses and try to suggest to stop them but if there are non just proceed
    3. how to pay off debt based on income and needs.
    so consider everything when it comes to my finances but be sensible.
    Here is the data on my income per month, expenses per month and overall debt/s. {user_data} and all numbers mentioned are Filipino Peso so just reffer to it as php
    
     create a final report on how my budget should look like
    
    Context: {context}

    Question: {question}
    """

    # Create Langchain chain
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        RunnableMap(
            {
                "context": lambda x: retriever.invoke(x["question"]),
                "question": lambda x: x["question"],
                "user_data": lambda x: x["user_data"]
            }
        )
        | prompt
        | gemini
        | list  # Convert output to string
    )
    # Run the chain
    response = chain.invoke({"question": "How should you save money for needs? or how should I allocate them", 
                                    "user_data": {"Expenses: transportation 1000, food 5000, vape = 500, cigs = 200", "Income=salary = 35000, non regular income on commissions = 1k-4k", "debt = 1000000"}}
                                       )
    # response_lines = response.splitlines()
    print(response)
if __name__ == "__main__":
    asyncio.run(main())