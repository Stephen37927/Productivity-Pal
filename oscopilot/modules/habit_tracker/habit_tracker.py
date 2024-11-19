import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from transformers import pipeline

from oscopilot import BaseModule
from oscopilot.prompts.Habit_Prompt import habit_prompt
from oscopilot.utils.database import DailyLogDatabase, HabitDatabase
from pymongo import DESCENDING
from oscopilot.utils.utils import send_chat_prompts

load_dotenv(override=True)
MODEL_NAME = os.getenv('HABIT_EXTRACTION_ENDPOINT')


class HabitTracker(BaseModule):
    def __init__(self):
        super().__init__()

    def fetch_recent_logs(self, user_id, top_k, days = -1, task=None):
        dailylog_db = DailyLogDatabase("Daily_logs")
        dailylog_db.collection.create_index([("Date", DESCENDING)])
        dailylog_db.collection.create_index(["user_id"])
        indexes = dailylog_db.collection.index_information()
        # print(indexes)
        query = {
            "user_id": user_id
        }
        if days > 0:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            start_timestamp = int(start_date.timestamp())
            end_timestamp = int(end_date.timestamp())
            print(start_timestamp, end_timestamp)
            query["Date"] = {"$gte": start_timestamp, "$lte": end_timestamp},
        pipeline = []
        if task is not None:
            task_embedding = dailylog_db.get_embedding(task)
            pipeline.append({
                "$search": {
                    "knnBeta": {
                        "vector": task_embedding,
                        "path": "embedding",
                        "k": top_k
                    }
                }
            })
        pipeline.append({"$match": query})
        pipeline.append({"$limit": top_k})
        logs = dailylog_db.find(pipeline)
        print(f"Find {len(logs)} logs")
        return logs

    def save_habit(self, habit):
        data = json.loads(habit)
        for key, value in data.items():
            habit_db = HabitDatabase(key)
            habit_db.insert(value)
        return "Habit saved successfully"

    def get_habit_from_logs(self, user_id, days =-1, top_k=-1, task=""):
        if task == "" and days == -1:
            return "Invaild request because both task and days are empty"
        logs = self.fetch_recent_logs(user_id=user_id, top_k=top_k, days=days, task=task)
        # self.llm.set_model_name(MODEL_NAME)
        if len(logs) == 0:
            return "No logs found"
        user_prompt = habit_prompt["USER_PROMPT"] + "\n " + "**Activities**: \n" + self.transfer_data_to_prompt(logs)
        response = send_chat_prompts(habit_prompt["USER_PROMPT"], user_prompt, self.llm, prefix="Overall")
        return response


if __name__ == '__main__':
    habit_tracker = HabitTracker()
    logs = habit_tracker.abstract_logs()
