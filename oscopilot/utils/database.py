from cmath import isnan

from matplotlib.backend_tools import cursors
# from matplotlib.backend_tools import cursors
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer
import pandas as pd
from datetime import datetime,timedelta
import json


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

    def insert(self, data,user_id):
        i = 0
        insert_count = 0
        for item in data:
            i = i+1
            for key, value in item.items():
                text = key + ": " + str(value)
            embedding = self.get_embedding(text)
            document = {**item,"user_id":user_id, "text": text, "embedding": embedding}
            try:
                self.collection.insert_one(document)
                insert_count = insert_count + 1
            except Exception as e:
                print(f"Error inserting document {i}: {e}")
                continue
        print(f"Inserted {insert_count} documents into the collection.")

    def find(self, pipeline, task="", user_id=1, limit=-1):
        cursors = self.collection.find(pipeline)
        cursors = cursors.limit(limit) if limit > 0 else cursors
        response = []
        for cursor in cursors:
            response.append(cursor)
        logs = []
        for item in response:
            log = {}
            for key, value in item.items():
                if key != "text" or key != "embedding":
                    log[key] = value
            logs.append(log)
        return logs

    def timestamp_to_date(self, timestamp, output_date_format):
        date_obj = datetime.fromtimestamp(timestamp)
        return date_obj.strftime(output_date_format)

    def date_to_timestamp(self, date_str, input_date_format):
        date_obj = datetime.strptime(date_str, input_date_format)
        return date_obj.timestamp()

class DailyLogDatabase(Database):
    def __init__(self, collection_name):
        super().__init__()
        self.collection = self.db[collection_name]

    def insert(self, data, user_id):
        i = 0
        insert_count = 0
        for item in data:
            i = i+1
            text = ""
            if "Active" in item:
                text = text+ "Activity: "+ str(item["Active"])+", "
            if "Type" in item:
                text = text + "Type: "+ str(item["Type"])+", "
            # if "Start Time" in item:
            #     one_week_seconds = 7 * 24 * 60 * 60  # 7天的秒数
            #     item["Start Time"] = int(item["Start Time"]) + one_week_seconds
            # if "End Time" in item:
            #     one_week_seconds = 7 * 24 * 60 * 60
            #     item["End Time"] = int(item["End Time"]) + one_week_seconds
            # if "Date" in item:
            #     one_week_seconds = 7 * 24 * 60 * 60
            #     item["Date"] = int(item["Date"]) + one_week_seconds
            embedding = self.get_embedding(text)
            document = {**item,"user_id": user_id, "text": text, "embedding": embedding}
            try:
                self.collection.insert_one(document)
                insert_count = insert_count + 1
            except Exception as e:
                print(f"Error inserting document {i}: {e}")
                continue
        print(f"Inserted {insert_count} documents into the collection.")

    def find(self, pipeline):
        cursors = self.collection.aggregate(pipeline)
        response = []
        for cursor in cursors:
            response.append(cursor)
        logs = []
        for item in response:
            log= {}
            for key, value in item.items():
                if key == "Active":
                    log["Active"] = value
                elif key == "Type":
                    log["Type"] = value
                elif key == "Start Time":
                    try:
                        log["Start Time"] = self.timestamp_to_date(value, "%Y-%m-%d %H:%M")
                    except:
                        pass
                elif key == "End Time":
                    try:
                        log["End Time"] = self.timestamp_to_date(value, "%Y-%m-%d %H:%M")
                    except:
                        pass
                elif key == "Date":
                    try:
                        log["Date"] = self.timestamp_to_date(value, "%Y-%m-%d")
                    except:
                        pass
            logs.append(log)
        return logs

class HabitDatabase(Database):
    def __init__(self, collection_name):
        super().__init__()
        self.collection = self.db[collection_name]
    def insert(self, data, user_id):
        i = 0
        insert_count = 0
        for item in data:
            i = i+1
            for key, value in item.items():
                text = key + ": " + str(value)
            embedding = self.get_embedding(text)
            document = {**item, "user_id":user_id, "text": text, "embedding": embedding}
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

            # 计算从当前时间到截止日期的持续时长（分钟）
            duration = (deadline - now).total_seconds() / 60

            # 使用 MongoDB 聚合查询最大值和最小值
            aggregation_pipeline = [
                {
                    "$addFields": {
                        "Duration": {
                            "$cond": [
                                {"$and": [{"$ifNull": ["$Start Time", False]}, {"$ifNull": ["$End Time", False]}]},
                                {
                                    "$divide": [
                                        {"$subtract": [
                                            {"$dateFromString": {"dateString": "$End Time", "format": "%Y%m%d%H%M"}},
                                            {"$dateFromString": {"dateString": "$Start Time", "format": "%Y%m%d%H%M"}}
                                        ]},
                                        60 * 1000  # 转换为分钟
                                    ]
                                },
                                None
                            ]
                        }
                    }
                },
                {"$match": {"Duration": {"$ne": None}}},  # 排除没有持续时间的记录
                {
                    "$group": {
                        "_id": None,
                        "max_duration": {"$max": "$Duration"},
                        "min_duration": {"$min": "$Duration"},
                    }
                }
            ]

            duration_stats = list(self.collection.aggregate(aggregation_pipeline))
            if not duration_stats:
                print("数据库中没有有效的持续时长记录。")
                return []

            max_duration = duration_stats[0]["max_duration"]
            min_duration = duration_stats[0]["min_duration"]

            # 动态调整误差范围
            if duration < min_duration:
                tolerance = max(10, min_duration * 0.1)
            elif duration > max_duration:
                tolerance = max(10, max_duration * 0.1)
            else:
                tolerance = max(10, duration * 0.2)

            # 匹配持续时长与用户输入接近的记录
            results = []
            logs = self.collection.find()
            for log in logs:
                if "Start Time" in log and "End Time" in log:
                    try:
                        start_time = datetime.strptime(log["Start Time"], "%Y%m%d%H%M")
                        end_time = datetime.strptime(log["End Time"], "%Y%m%d%H%M")
                        log_duration = (end_time - start_time).total_seconds() / 60

                        # 打印调试信息
                        print(
                            f"记录 {log['Name']} 的时长: {log_duration:.2f} 分钟, 目标时长: {duration:.2f} 分钟, 容差范围: ±{tolerance:.2f} 分钟")

                        # 判断持续时长是否在容许误差范围内
                        if abs(log_duration - duration) <= tolerance:
                            results.append(log)
                    except Exception as e:
                        print(f"Error processing log: {log}, Error: {e}")
                else:
                    print(f"跳过无效记录: {log}")

            return results

        except Exception as e:
            print(f"Error during find_by_deadline: {e}")
            return []

class DeadlineDatabase(Database):
    def __init__(self,collection_name):
        super().__init__()
        self.collection = self.db[collection_name]
    def insert(self,data,user_id):
        i = 0
        insert_count = 0
        for item in data:
            i = i+1
            text = ""
            if "Subtasks" not in item:
                item["Subtasks"] = []
            for key, value in item.items():
                if key == "Title":
                    text = text + "Title: " + value + "; "
                elif key == "Description":
                    text = text + "Description: " + value + "; "
                elif key == "Deadline":
                    item["Deadline"] = self.date_to_timestamp(value, "%Y%m%d%H%M")
            embedding = self.get_embedding(text)
            document = {**item, "user_id": user_id, "text": text, "embedding": embedding}
            try:
                self.collection.insert_one(document)
                insert_count = insert_count + 1
            except Exception as e:
                print(f"Error inserting document {i}: {e}")
                continue
        print(f"Inserted {insert_count} documents into the collection.")

    def find(self, pipeline, task="", user_id=1, limit=-1):
        cursors = self.collection.find(pipeline)
        cursors = cursors.limit(limit) if limit > 0 else cursors
        response = []
        for cursor in cursors:
            response.append(cursor)
        logs = []
        for item in response:
            log = {}
            for key, value in item.items():
                if key == "Title":
                    log["Title"] = value
                elif key == "Description":
                    log["Description"] = value
                elif key == "Deadline":
                    try:
                        date_obj = datetime.strptime(value, "%Y%m%d%H%M")
                        log["Deadline"] = date_obj.strftime("%Y-%m-%d %H:%M")
                    except:
                        pass
                elif key == "Status":
                    try:
                        log["Status"] = value
                    except:
                        pass
            logs.append(log)
        return logs





if __name__ == '__main__':
    deadlines = [
        {
        "Title": "OS-CoPilot Demo Presentation",
        "Description": "Prepare a demo presentation for OS-CoPilot. Include coding, presentation slides, and a live demo.",
        "Deadline": "202411251900",
        "Status": 10
        },
        {
            "Title": "Data Mining Assignment2",
            "Description": "3 subtasks: 1. Evaluate car sales data via Weka. 2. Assoication rule mining. 3. Clustering.",
            "Deadline": "202411272359",
            "Status": 00
        },
        {
            "Title": "CV Reviewer",
            "Description": "Review the CVs of the applicants for the Data Scientist position.",
            "Deadline": "202411301700",
            "Status": 00
        },
        {
            "Title": "Weekend Getaway Planning",
            "Description": "Plan and finalize the itinerary for a weekend getaway with friends. Book transportation and accommodation.",
            "Deadline": "202412102000",
            "Status": 00
        },
        {
            "Title": "Team Meeting Presentation",
            "Description": "Prepare a brief presentation for the team's weekly sync. Include project updates and upcoming plans.",
            "Deadline": "202411201000",
            "Status": 10
        },
        {
            "Title": "Christmas Holiday Planning",
            "Description": "Plan the Christmas holiday activities, including gift shopping, travel arrangements, and dinner preparation.",
            "Deadline": "202412201800",
            "Status": 00
        },
        {
            "Title": "Deep Learning Course Final Exam",
            "Description": "The final examination on deep learning, including basic information, CNN, GNN, and RNN.",
            "Deadline": "202412141830",
            "Status": 00
        }
    ]

    deadlines_db = DeadlineDatabase("Deadlines")
    deadlines_db.insert(deadlines, user_id=1)

    # data_list = []
    # with open("output_data1.jsonl", 'r', encoding='utf-8') as f:
    #     for line in f:
    #         # 每一行都是一个 JSON 对象
    #         data_list.append(json.loads(line.strip()))
    # daily_log_db = DailyLogDatabase("Daily_logs")
    # daily_log_db.insert(data_list, user_id=1)
