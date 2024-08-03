# src/crud/interaction_crud.py

from pymongo import ReturnDocument
from src.db.models.interaction import Interaction
from src import Database
from bson import ObjectId
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the database instance
db = Database().get_database()

class InteractionCRUD:
    @staticmethod
    async def create_interaction(interaction_data: dict) -> Interaction:
        """Create a new interaction in the database."""
        interaction = Interaction(**interaction_data)
        try:
            result = await db.interactions.insert_one(interaction.model_dump(by_alias=True))
            logging.info(f"Inserted interaction ID: {result.inserted_id}")
            return interaction
        except Exception as e:
            logging.error(f"Error creating interaction: {e}")
            raise

    @staticmethod
    async def get_interaction(interaction_id: str) -> Interaction:
        """Retrieve an interaction from the database by its ID."""
        try:
            interaction = await db.interactions.find_one({"_id": ObjectId(interaction_id)})
            if interaction:
                return Interaction(**interaction)
            else:
                logging.info(f"Interaction with ID {interaction_id} not found.")
                return None
        except Exception as e:
            logging.error(f"Error retrieving interaction: {e}")
            raise

    @staticmethod
    async def update_interaction(interaction_id: str, update_data: dict) -> Interaction:
        """Update an existing interaction in the database."""
        try:
            updated_interaction = await db.interactions.find_one_and_update(
                {"_id": ObjectId(interaction_id)},
                {"$set": update_data},
                return_document=ReturnDocument.AFTER
            )
            if updated_interaction:
                return Interaction(**updated_interaction)
            else:
                logging.info(f"Interaction with ID {interaction_id} not found for update.")
                return None
        except Exception as e:
            logging.error(f"Error updating interaction: {e}")
            raise

    @staticmethod
    async def delete_interaction(interaction_id: str) -> bool:
        """Delete an interaction from the database by its ID."""
        try:
            result = await db.interactions.delete_one({"_id": ObjectId(interaction_id)})
            if result.deleted_count == 1:
                logging.info(f"Interaction with ID {interaction_id} deleted successfully.")
                return True
            else:
                logging.info(f"Interaction with ID {interaction_id} not found for deletion.")
                return False
        except Exception as e:
            logging.error(f"Error deleting interaction: {e}")
            raise
