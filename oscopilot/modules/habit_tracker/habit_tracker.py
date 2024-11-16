import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

from oscopilot import BaseModule
from oscopilot.prompts.Habit_Prompt import habit_prompt
from oscopilot.utils.database import DailyLogDatabase
from pymongo import DESCENDING
from oscopilot.utils.utils import send_chat_prompts

load_dotenv(override=True)
ENDPOINT = os.getenv('HABIT_EXTRACTION_ENDPOINT')

class HabitTracker(BaseModule):
    def __init__(self):
        super().__init__()
    def fetch_recent_logs(self, days):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        start_date = start_date.strftime("%Y%m%d")
        print("start_date: ", start_date)
        end_date = end_date.strftime("%Y%m%d")
        print("end_date: ", end_date)
        datalog_db = DailyLogDatabase("daily_logs")
        # logs = datalog_db.find({"Date": {"$gte": start_date, "$lte": end_date}})
        logs = datalog_db.find({"Date": {"$gte": start_date, "$lte": end_date}}).sort("Date", DESCENDING)
        return logs

    def save_habit(self, habit):
        habit_db = DailyLogDatabase("habits")
        habit_db.insert(habit)

    def get_habit_from_logs(self):
        logs = self.fetch_recent_logs(7)
        self.llm.set_endpoint(ENDPOINT)
        user_prompt = {
            "Habits_Input": logs,
            "Prompt": habit_prompt["GAIA_ANSWER_EXTRACTOR_PROMPT"]
        }
        response = send_chat_prompts("sys_prompt", user_prompt, self.llm, prefix="Overall")
        print(response)
        return response


if __name__ == '__main__':
    habit_tracker = HabitTracker()
    logs = habit_tracker.abstract_logs()
    print(logs)
