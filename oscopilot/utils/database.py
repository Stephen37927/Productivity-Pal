from cmath import isnan

# from matplotlib.backend_tools import cursors
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer
import pandas as pd
from datetime import datetime,timedelta
from sqlalchemy.dialects.mysql import insert

load_dotenv(override=True)
MODEL_NAME = os.getenv('MODEL_NAME')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ORGANIZATION = os.getenv('OPENAI_ORGANIZATION')
BASE_URL = os.getenv('OPENAI_BASE_URL')
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

class Database:
    def __init__(self):
        try:
            self.client = MongoClient(CONNECTION_STRING)
            self.db = self.client['productivity_pal']
            self.model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)
            Database.model_loaded = True
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise

    def get_embedding(self, data):
        """Generates vector embeddings for the given data."""
        try:
            embedding = self.model.encode(data)
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise
        return embedding.tolist()

    def get_collection(self, collection_name):
        """Helper method to fetch a collection from the database."""
        try:
            return self.db[collection_name]
        except Exception as e:
            print.error(f"Error fetching collection {collection_name}: {e}")
            raise

    def insert(self, data):
        i = 0
        insert_count = 0
        for item in data:
            i = i+1
            for key, value in item.items():
                text = key + ": " + str(value)
            embedding = self.get_embedding(text)
            document = {**item, "text": text, "embedding": embedding}
            try:
                self.collection.insert_one(document)
                insert_count = insert_count + 1
            except Exception as e:
                print(f"Error inserting document {i}: {e}")
                continue
        print(f"Inserted {insert_count} documents into the collection.")

    def find_by_deadline(self, deadline_str):
        """
        Finds documents with a deadline matching or earlier than the specified deadline.

        Parameters:
        deadline (str): The deadline date in ISO 8601 format (e.g., "2024-11-30").

        Returns:
        list: A list of matching documents.
        """

        try:
            # 将截止日期字符串转换为 datetime 对象
            deadline = datetime.strptime(deadline_str, "%Y%m%d%H%M")
            now = datetime.now()

            # 计算从当前时刻到截止日期的持续时长（分钟）
            duration = (deadline - now).total_seconds() / 60

            # 查询数据库中的所有日志
            logs = list(self.collection.find())

            # 找到持续时长与计算结果接近的记录（±5分钟）
            results = []
            for log in logs:
                # 检查记录是否包含 "Start Time" 和 "End Time"
                if "Start Time" not in log or "End Time" not in log:
                    continue  # 跳过不完整的记录

                try:
                    start_time = datetime.strptime(log["Start Time"], "%Y%m%d%H%M")
                    end_time = datetime.strptime(log["End Time"], "%Y%m%d%H%M")
                    log_duration = (end_time - start_time).total_seconds() / 60

                    # 判断持续时长是否在 ±60 分钟范围内
                    if abs(log_duration - duration) <= 60:
                        results.append(log)
                except Exception as e:
                    print(f"Error processing log: {log}, Error: {e}")
                    continue

            return results
        except Exception as e:
            print(f"Error during find_by_deadline: {e}")
            return []


class DailyLogDatabase(Database):
    def __init__(self, collection_name):
        super().__init__()
        self.collection = self.db[collection_name]

    def insert(self, data):
        i = 0
        insert_count = 0
        for item in data:
            i = i+1
            text = "Activity: "+ str(item["Name"])+", "+"Type: "+ str(item["Type"])
            embedding = self.get_embedding(text)
            document = {**item, "text": text, "embedding": embedding}
            try:
                self.collection.insert_one(document)
                insert_count = insert_count + 1
            except Exception as e:
                print(f"Error inserting document {i}: {e}")
                continue
        print(f"Inserted {insert_count} documents into the collection.")

    def find(self, query, limit = -1):
        cursors = self.collection.find(query)
        cursors = cursors.limit(limit) if limit > 0 else cursors
        response = []
        for cursor in cursors:
            response.append(cursor)
        logs = []
        for item in response:
            log= {}
            for key, value in item.items():
                if key == "Name":
                    log["Active:"] = value
                elif key == "Type":
                    log["Type:"] = value
                elif key == "Start Time":
                    try:
                        date_obj = datetime.strptime(value, "%Y%m%d%H%M")
                        log["Start Time:"] = date_obj.strftime("%Y-%m-%d %H:%M")
                    except:
                        pass
                elif key == "End Time":
                    try:
                        date_obj = datetime.strptime(value, "%Y%m%d%H%M")
                        log["End Time:"] = date_obj.strftime("%Y-%m-%d %H:%M")
                    except:
                        pass
                elif key == "Date":
                    try:
                        date_obj = datetime.strptime(value, "%Y%m%d")
                        log["Date:"] = date_obj.strftime("%Y-%m-%d")
                    except:
                        pass
            logs.append(log)
        return logs

class HabitDatabase(Database):
    def __init__(self, collection_name):
        super().__init__()
        self.collection = self.db[collection_name]
    def insert(self, data):
        i = 0
        insert_count = 0
        for item in data:
            i = i+1
            for key, value in item.items():
                text = key + ": " + str(value)
            embedding = self.get_embedding(text)
            document = {**item, "text": text, "embedding": embedding}
            try:
                self.collection.insert_one(document)
                insert_count = insert_count + 1
            except Exception as e:
                print(f"Error inserting document {i}: {e}")
                continue
        print(f"Inserted {insert_count} documents into the collection.")

if __name__ == '__main__':
    data = df = pd.read_csv("./data/datalog1.csv")
    data = df.to_dict(orient='records')
    input_data = []
    for item in data:
        input = {}
        for key, value in item.items():
            starttime = 0
            endtime = 0
            if key == "Name":
                input["Name"] = value
            if key == "类型":
                input["Type"] = value
            if key == "开始时间":
                try:
                    date_obj = datetime.strptime(value, "%B %d, %Y %I:%M %p (GMT+8)")
                    date_obj += timedelta(weeks=7)
                    input["Start Time"] = date_obj.strftime("%Y%m%d%H%M")
                    starttime = int(input["Start Time"])
                except:
                    pass
            if key == "结束时间":
                try:
                    date_obj = datetime.strptime(value, "%B %d, %Y %I:%M %p (GMT+8)")
                    date_obj += timedelta(weeks=7)
                    input["End Time"] = date_obj.strftime("%Y%m%d%H%M")
                    endtime = int(input["End Time"])
                    int["Duration"] = endtime - starttime
                except:
                    pass
            if key == "日期":
                try:
                    date_obj = datetime.strptime(value, "%Y/%m/%d")
                    date_obj += timedelta(weeks=7)
                    input["Date"] = date_obj.strftime("%Y%m%d")
                except:
                    pass
        input_data.append(input)

    log_db = DailyLogDatabase("daily_logs")
    log_db.insert(input_data)