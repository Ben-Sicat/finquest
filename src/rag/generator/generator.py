import asyncio
import os
from typing import List
import logging

from dotenv import load_dotenv
from langchain.schema import Document
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_google_vertexai import ChatVertexAI, VertexAIEmbeddings
from src.db.CRUD.document_crud import DocumentCRUD
from src.db.CRUD.user_crud import UsersCRUD # Import UsersCrud
from langchain.schema.runnable import RunnableMap
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from motor.motor_asyncio import AsyncIOMotorClient

from src.rag.generator.templates import get_template  # Import the template function

# Output parser
output_parser = StrOutputParser()

# Load environment variables
load_dotenv()

# Constants
DB_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = "documents"
CONNECTION_STRING = os.getenv('MONGO_URL')

# Initialize Vertex AI Embeddings
embeddings = VertexAIEmbeddings(
    model="text-embedding-004", project="finquest", location="us-central1"
)

async def fetch_all_documents() -> List[str]:
    """Fetches all documents from the specified MongoDB collection."""
    # Use DocumentCRUD to get all documents
    documents = await DocumentCRUD.get_all_documents_content()
    content_list = [doc['content'] for doc in documents]
    logging.info(f"Fetched {len(content_list)} documents.")
    return content_list

async def initialize_db():
    """Initializes the in-memory database with embedded documents."""
    # Fetch documents directly
    docs = await fetch_all_documents()

    # Extract content from documents and embed them
    db = DocArrayInMemorySearch.from_texts(
        docs, embeddings
    )
    return db

# Initialize Vertex AI Chat Model
gemini = ChatVertexAI(
    model="gemini-1.5-flash-001", project="finquest", location="us-central1", max_output_tokens=1500
)

async def create_retriever() -> DocArrayInMemorySearch:
    """Create a retriever from the initialized database."""
    db = await initialize_db()
    retriever = db.as_retriever(
        search_type="similarity", search_kwargs={"score_threshold": 0.4, "k": 3}
    )
    return retriever

async def ask_general_advisory(question: str) -> str:
    """Ask a general financial advisory question."""
    retriever = await create_retriever()

    # Load the general advisory template
    template = get_template("general")

    # Create Langchain chain for general advisory
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        RunnableMap(
            {
                "context": lambda x: retriever.invoke(x["question"]),
                "question": lambda x: x["question"],
            }
        )
        | prompt
        | gemini
        | list  # Convert output to string
    )

    # Run the chain
    response = chain.invoke({"question": question})
    return response

async def fetch_user_financial_data(user_id: str) -> str:
    """Fetch the user's financial data from MongoDB and aggregate it into a single string."""
    # Use UsersCrud to fetch user data
    user_data = await UsersCRUD.get_user(user_id)

    # Access attributes directly and handle missing data
    income = user_data.income if hasattr(user_data, 'income') else 'Not specified'
    debt = user_data.debt if hasattr(user_data, 'debt') else 'Not specified'
    expenses = user_data.expenses if hasattr(user_data, 'expenses') else 'Not specified'

    # Aggregate into a single string
    aggregated_data = f"Income: {income}; Debt: {debt}; Expenses: {expenses}"
    logging.info(f"Fetched financial data for user {user_id}: {aggregated_data}")

    # return aggregated_data
    
    return aggregated_data

async def generate_specific_advisory(user_id: str, question: str) -> str:
    """Generate specific financial advice with user data."""
    retriever = await create_retriever()

    # Load the specific advisory template
    template = get_template("specific")

    # Fetch user data and aggregate it
    user_data = await fetch_user_financial_data(user_id)

    # Create Langchain chain for specific advisory
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        RunnableMap(
            {
                "context": lambda x: retriever.invoke(x["question"]),
                "question": lambda x: x["question"],
                "user_data": lambda x: x["user_data"],
            }
        )
        | prompt
        | gemini
        | list  # Convert output to string
    )

    # Run the chain
    response = chain.invoke({"question": question, "user_data": user_data})
    return response

async def main():
    # Example of asking a general advisory question
    # general_response = await ask_general_advisory("What are the best practices for saving money?")
    # print("General Advisory Response:")
    # print(general_response)

    # Example of generating specific financial advice for a user
    specific_response = await generate_specific_advisory(
        user_id="66adfab6844c979caa396f04",
        question="How should I allocate my budget so that i can buy the new iphone in 2 months"
    )
    print("Specific Financial Advisory Response:")
    print(specific_response)

if __name__ == "__main__":
    asyncio.run(main())
