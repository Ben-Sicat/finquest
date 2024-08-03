# src/db/test_insert.py

from src.database import Database
from src.db.models import Literature, Document, Users, Interaction
from src.db.CRUD.document_crud import DocumentCRUD
from src.db.CRUD.user_crud import UsersCRUD
import asyncio
import logging
from bson import ObjectId

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def insert_test_data():
    # Create database connection
    db = Database()
    database = db.get_database()
    print(database)

    # # Test data for Literature collection
    # literature_data = {
    #     "title": "A Study on Artificial Intelligence",
    #     "content": "Artificial Intelligence is rapidly evolving...",
    #     "url": "http://example.com/ai-study",
    #     "created_at": "2024-07-25",
    #     "updated_at": "2024-07-25"
    # }

    # # Convert to Pydantic model
    # literature = Literature(**literature_data)

    # try:
    #     # Insert literature data into MongoDB
    #     result = await database.literature.insert_one(literature.model_dump(by_alias=True))
    #     logging.info(f"Inserted literature document ID: {result.inserted_id}")
    # except Exception as e:
    #     logging.error(f"Error inserting literature: {e}")

    # Test data for Document collection
    # document_data = {
    #     "title": "bullshit Deep machine Learning",
    #     "content": "Deep Learning techniques have transformed AI and lana del rey...",
    #     "author": "joe Doe",
    #     "created_at": "2024-07-25",
    #     "updated_at": "2024-07-25",
    #     "embedding": [[0.1, 0.2, 0.3, 0.4, 0.5], [0.6, 0.7, 0.8, 0.9, 1.0], [1.1, 1.2, 1.3, 1.4, 1.5]]

 
    # }

    # # Convert to Pydantic model
    # document = Document(**document_data)

    # try:
    #     # Insert document data into MongoDB
    #     result = await database.documents.insert_one(document.model_dump(by_alias=True))
    #     logging.info(f"Inserted document ID: {result.inserted_id}")
    # except Exception as e:
    #     logging.error(f"Error inserting document: {e}")
    # now we're gonna create a test to see if the get all documents function works
    # try:
    #     documents = await DocumentCRUD.get_all_documents_content()
    #     print(documents)
    # except Exception as e:
    #     logging.error(f"Error getting documents: {e}")
    #     return []  
    # # test the update on document with id 66a6ae4a0b32072336c2fb33
    # from bson import ObjectId
    id = "66adfab6844c979caa396f04"
    try:
        data = await UsersCRUD.get_user(id)
        print(data)
    except Exception as e:
        logging.error(f"Error getting user: {e}")
        return []

    # document_id = "66a6ae4a0b32072336c2fb33"
    # object_id  = ObjectId(document_id)
    # document_id = object_id
    # update_data = {
    #     "title": "Understanding Deep Learning by ben",
    #     "content": "Deep Learning techniques have transformed AI... by ben sicat",
    #     "author": "Ben Sic",
    #     "created_at": "2024-07-25",
    #     "updated_at": "2024-07-25",
    #     "embedding": [[0.1, 0.2, 0.3, 0.4, 0.5], [0.6, 0.7, 0.8, 0.9, 1.0], [1.1, 1.2, 1.3, 1.4, 1.5]]
    # }

    # # Convert to Pydantic model (assuming Document is the correct model)
    # document = Document(**update_data)

    # try:
    #     # Update document data in MongoDB
    #     result = await DocumentCRUD.update_document(document_id, document.model_dump(by_alias=True))
    #     if result:
    #         logging.info(f"Updated document ID: {document_id}")
    #     else:
    #         logging.info(f"Document with ID {document_id} not found for update.")
    # except Exception as e:
    #     logging.error(f"Error updating document: {e}")

    # document_id = "66a6ae4a0b32072336c2fb33"
    # object_id = ObjectId(document_id)

    # # Use object_id for querying
    # result = await database.documents.find_one({"_id": object_id})
    # print(result)

    # Test data for User collection
    # user_data = {
    #     "name": "gian",
    #     "email": "janedoe@example.com",
    #     "full_name": "gian",
    #     "password": "123",
    #     "expenses": "Expenses: transportation 1000, food 5000, vape = 500, cigs = 200",
    #     "income": "Income=salary = 35000, non regular income on commissions = 1k-4k",
    #     "debt": "1000000"
        
    # }

    # # # Convert to Pydantic model
    # user = Users(**user_data)

    # try:
    #     # Insert user data into MongoDB
    #     result = await database.users.insert_one(user.model_dump(by_alias=True))
    #     logging.info(f"Inserted user ID: {result.inserted_id}")
    # except Exception as e:
    #     logging.error(f"Error inserting user: {e}")
    
    ##

    # # Test data for Interaction collection
    # interaction_data = {
    #     "user_id": str(user.id),
    #     "query": "What is AI?",
    #     "response": "AI stands for Artificial Intelligence...",
    #     "timestamp": "2024-07-25T12:00:00"
    # }

    # # Convert to Pydantic model
    # interaction = Interaction(**interaction_data)

    # try:
    #     # Insert interaction data into MongoDB
    #     result = await database.interactions.insert_one(interaction.model_dump(by_alias=True))
    #     logging.info(f"Inserted interaction ID: {result.inserted_id}")
    # except Exception as e:
    #     logging.error(f"Error inserting interaction: {e}")
    
    # test data for embedding collection
    # embedding_data = {
    #     "document_id": "1",
    #     "embeddings": [0.1, 0.2, 0.3, 0.4, 0.5]
    # }
    
    # # Convert to Pydantic model
    # embedding = Embeddings(**embedding_data)
    
    # try:
    #     # Insert embedding data into MongoDB
    #     result = await database.embeddings.insert_one(embedding.model_dump(by_alias=True))
    #     logging.info(f"Inserted embedding ID: {result.inserted_id}")
    # except Exception as e:
    #     logging.error(f"Error inserting embedding: {e}")
        
    

# Run the asynchronous test_insert function
if __name__ == "__main__":
    asyncio.run(insert_test_data())
