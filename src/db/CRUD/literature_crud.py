# src/crud/literature_crud.py

from pymongo import ReturnDocument
from src.db.models.literature import Literature
from src import Database
from bson import ObjectId
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LiteratureCRUD:
    @staticmethod
    async def create_literature(literature_data: dict) -> Literature:
        literature = Literature(**literature_data)
        try:
            results = await Database().get_database().literature.insert_one(literature.model_dump(by_alias=True))
            logging.info(f"Inserted literature ID: {results.inserted_id}")
            return literature
        except Exception as e:
            logging.error(f"Error inserting literature: {e}")
            return None

    @staticmethod
    async def get_literature(literature_id: str) -> Literature:
        try:
            literature = await Database().get_database().literature.find_one({"_id": ObjectId(literature_id)})
            if literature:
                return Literature(**literature)
        except Exception as e:
            logging.error(f"Error getting literature: {e}")
            return None

    @staticmethod
    async def update_literature(literature_id: str, literature_data: dict) -> Literature:
        try:
            literature = await Database().get_database().literature.find_one_and_update(
                {"_id": ObjectId(literature_id)},
                {"$set": literature_data},
                return_document=ReturnDocument.AFTER
            )
            if literature:
                return Literature(**literature)
            else:
                logging.info(f"Literature with ID {literature_id} not found")
                return None
        except Exception as e:
            logging.error(f"Error updating literature: {e}")
            return None

    @staticmethod
    async def delete_literature(literature_id: str) -> bool:
        try:
            result = await Database().get_database().literature.delete_one({"_id": ObjectId(literature_id)})
            if result.deleted_count:
                logging.info(f"Literature with ID {literature_id} deleted")
                return True
            else:
                logging.info(f"Literature with ID {literature_id} not found")
                return False
        except Exception as e:
            logging.error(f"Error deleting literature: {e}")
            raise e