from numpy.lib.function_base import insert

from oscopilot.utils.database import  DailyLogDatabase
import pandas as pd

if __name__ == '__main__':
    daily_log_db = DailyLogDatabase("DailyLogs")
    daily_logs = pd.read_csv("../data/output_data1.jsonl")
    insert_count = 0
    for log in daily_logs:
        if daily_log_db.insert_one_log(log)!=None:
            insert_count += 1

    print(f"Inserted {insert_count} logs")