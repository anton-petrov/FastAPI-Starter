import asyncio
import logging
from pprint import pprint
from typing import Any, Dict, List

import motor.motor_asyncio
from pydantic import BaseModel

from project.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoDB:
    def __init__(self, connection: str, db: str = "", collection: str = ""):
        self.client = MongoDB.__connect_to_mongo(connection)
        self.db = self.client[db]
        self.collection = self.db[collection]
        self.current_database_name = db
        self.current_collection_name = collection

    def set_database(self, db_name: str) -> Any:
        self.db = self.client[db_name]
        self.current_database_name = db_name
        return self.db

    def set_collection(self, collection_name: str) -> None:
        self.collection = self.db[collection_name]
        self.current_collection_name = collection_name

    @staticmethod
    def __connect_to_mongo(connection: str) -> Any:
        return motor.motor_asyncio.AsyncIOMotorClient(connection)

    async def insert(self, document: dict) -> str | Any:
        if document is None:
            return None
        collection = self.collection
        result = await collection.insert_one(document)
        return result.inserted_id

    async def find(self, find: dict) -> Dict | None:
        document = await self.collection.find_one(find)
        return document

    async def find_all(self, find={}, cls=None) -> List[Any]:
        result = []
        cursor = self.collection.find(find)
        async for document in cursor:
            if cls is not None:
                result.append(cls(**document))
            else:
                result.append(document)
        return result

    async def insert_one(self, document: Dict) -> Dict[str, Any] | Any:
        document = await self.collection.insert_one(document)
        return document

    async def remove(self, document: dict) -> Any:
        await self.collection.delete_one(document)

    async def update(self, document: dict, update_data: Dict) -> Dict | Any:
        await self.collection.update_one(document, {"$set": update_data})
        document = await self.collection.find_one(document)
        return document


# Test code
async def test_mongo(mongo: MongoDB):
    class TestClass(BaseModel):
        test_key = ""

    await mongo.insert({"test_key": "test_value"})
    await mongo.insert({"test_key1": "test_value1"})
    await mongo.update({"test_key": "test_value"}, {"test_key": "test_value777"})
    list1 = await mongo.find_all(TestClass)
    pprint(list1)


def test():
    db_name = "test_database"
    collection_name = "test_collection"
    mongo = MongoDB(str(settings.mongo_url), db_name, collection_name)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_mongo(mongo))


if __name__ == "__main__":
    # test code
    test()
