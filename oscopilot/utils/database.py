from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv(override=True)
MODEL_NAME = os.getenv('MODEL_NAME')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ORGANIZATION = os.getenv('OPENAI_ORGANIZATION')
BASE_URL = os.getenv('OPENAI_BASE_URL')
CONNECTION_STRING = os.getenv('CONNECTION_STRING')
def get_database():

    # 使用 MongoClient 创建连接。您可以导入 MongoClient 或者使用 pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # 为我们的示例创建数据库（我们将在整个教程中使用相同的数据库
    return client['test1']
class Database:
    def __init__(self,database):
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client[database]

    def insert(self, collection, data, many=False):
        try:
            collection = self.db[collection]
            if many:
                result = collection.insert_many(data)
                print(f"{len(result.inserted_ids)} documents inserted successfully.")
            else:
                result = collection.insert_one(data)
                print(f"Document inserted successfully with id: {result.inserted_id}")
        except Exception as e:
            print(f"An error occurred during insert: {e}")

    def delete(self, collection, query, many=False):
        try:
            collection = self.db[collection]
            if not many:
                result = collection.delete_one(query)
                print(f"{result.deleted_count} document deleted.")
            else:
                result = collection.delete_many(query)
                print(f"{result.deleted_count} document(s) deleted.")
        except Exception as e:
            print(f"An error occurred during delete: {e}")

    def find(self, collection, query={}, projection=None):
        try:
            collection = self.db[collection]
            result = collection.find(query, projection)
            return list(result)
        except Exception as e:
            print(f"An error occurred during find: {e}")
            return []

class LogDatabase(Database):
    def __init__(self):
        super().__init__("logs")

    def insert_log(self, collection ,data, many=False):
        self.insert(collection, data, many)

    def delete_log(self, collection, query, many=False):
        self.delete(collection, query, many)
    

if __name__ == '__main__':
    db = Database("nlp")
    db.insert('logs', {'name': 'test'})