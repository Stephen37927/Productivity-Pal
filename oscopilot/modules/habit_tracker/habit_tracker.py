import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
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

    def fetch_recent_logs(self, days, limit=-1):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        start_date = start_date.strftime("%Y%m%d")
        end_date = end_date.strftime("%Y%m%d")
        datalog_db = DailyLogDatabase("daily_logs")
        datalog_db.collection.create_index([("Date", DESCENDING)])
        query = {"Date": {"$gte": start_date, "$lte": end_date}}
        logs = datalog_db.find(query, limit=limit)
        return logs

    def save_habit(self, habit):
        data = json.loads(habit)
        for key, value in data.items():
            habit_db = HabitDatabase(key)
            habit_db.insert(value)
        return "Habit saved successfully"

    def get_habit_from_logs(self):
        logs = self.fetch_recent_logs(7, limit=15)
        # self.llm.set_model_name(MODEL_NAME)
        user_prompt = habit_prompt["USER_PROMPT"] + "\n " + "**Activities**: \n" + self.transfer_data_to_prompt(logs)
        response = send_chat_prompts(habit_prompt["USER_PROMPT"], user_prompt, self.llm, prefix="Overall")
        return response


if __name__ == '__main__':
    habit_tracker = HabitTracker()
    logs = habit_tracker.abstract_logs()
