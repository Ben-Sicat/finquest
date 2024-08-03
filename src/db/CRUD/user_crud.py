from pymongo import ReturnDocument
from src.db.models.users import Users
from src import Database
from bson import ObjectId
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

db = Database().get_database()
class UsersCRUD:
    @staticmethod
    async def create_user(user_data: dict) -> Users:
        user = Users(**user_data)
        try:
            results = await db.users.insert_one(user.model_dump(by_alias=True))
            logging.info(f"Inserted user ID: {results.inserted_id}")
            return user
        except Exception as e:
            logging.error(f"Error inserting user: {e}")
            return None
    @staticmethod
    async def get_user(user_id: str) -> Users:
        try:
            user = await db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                return Users(**user)
        except Exception as e:
            logging.error(f"Error getting user: {e}")
            return None
    @staticmethod
    async def update_user(user_id: ObjectId, user_data: dict) -> Users:
        update_data = {key: value for key, value in user_data.items() if key != "_id"}
        print(user_id)
        logging.info(f"document_id: {user_id}")
        #now we need to parse document_id to string
        # document_id = str(document_id)
        try:
            document = await db.documents.find_one_and_update(
                {"_id": user_id},
                {"$set": update_data},
                return_document=ReturnDocument.AFTER
            )
            if document:
                return Users(**document)
            else:
                logging.info(f"Document with ID {user_id} not found")
                return None
        except Exception as e:
            logging.error(f"Error updating document: {e}")
            return None
    @ staticmethod
    async def delete_user(user_id: str) -> bool:
        try:
            result = await db.users.delete_one({"_id": ObjectId(user_id)})
            if result.deleted_count:
                logging.info(f"User with ID {user_id} deleted")
                return True
            else:
                logging.info(f"User with ID {user_id} not found")
                return False
        except Exception as e:
            logging.error(f"Error deleting user: {e}")
            raise e