from datetime import datetime, timedelta

from transformers import pipeline

from oscopilot.utils.database import DailyLogDatabase
from pymongo import DESCENDING

class HabitTracker():
    def __init__(self):
        pass
    def abstract_logs_in_previous_days(self, days):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        start_date = start_date.strftime("%Y%m%d")
        print("start_date: ", start_date)
        end_date = end_date.strftime("%Y%m%d")
        print("end_date: ", end_date)
        datalog_db = DailyLogDatabase("daily_logs")
        # logs = datalog_db.find({"Date": {"$gte": start_date, "$lte": end_date}})
        logs = datalog_db.find({"Date": {"$gte": start_date, "$lte": end_date}})
        return logs

    def save_habit(self, habit):
        habit_db = DailyLogDatabase("habits")
        habit_db.insert(habit)
    def get_and_save_habit(self):
        logs = self.abstract_logs_in_previous_days(7)



if __name__ == '__main__':
    habit_tracker = HabitTracker()
    logs = habit_tracker.abstract_logs()
    print(logs)
