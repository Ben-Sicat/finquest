import os
import logging
from pymongo import MongoClient
import motor.motor_asyncio
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

class Database:
    def __init__(self):
        mongo_url = os.environ.get("MONGO_URL")
        logging.info(f"MONGO_URL: {mongo_url}")

        if not mongo_url:
            logging.warning("WARNING: MONGO_URL environment variable not found. Using default (localhost).")
            mongo_url = "mongodb://localhost:27017/"

        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
            self.db = self.client["finquest"]  
        except Exception as e:
            logging.error(f"Error connecting to MongoDB: {e}")
            raise ConnectionError(f"Error connecting to MongoDB: {e}")

    def get_database(self):
        return self.db

    def get_collection(self, collection_name):
        return self.db[collection_name]

    async def check_connection(self):
        try:
            await self.db.command({"serverStatus": 1})
            logging.info("Connected to database")
            return True
        except Exception as e:
            logging.error(f"Error checking connection: {e}")
            return False

async def main():
    db = Database()
    database = db.get_database()
    logging.info(f"Database name: {database.name}")

    if await db.check_connection():
        print("Connected to database")
    else:
        print("Failed to connect to database")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
