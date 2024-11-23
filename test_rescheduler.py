from oscopilot.modules.schedule_maker.rescheduler import Rescheduler
from oscopilot.prompts.Schedule_Prompt import schedule_prompt
import json
from datetime import datetime, timedelta

user_id = 1
reschedule_time = "2023-11-17 10:00"
start_time = datetime.strptime("2023-11-17 00:00", "%Y-%m-%d %H:%M")
deadline = datetime.strptime("2023-11-20 23:59", "%Y-%m-%d %H:%M")
rescheduler = Rescheduler(user_id, reschedule_time, schedule_prompt)
new_schedule = rescheduler.execute_reschedule(start_time, deadline)
print("重新调度的任务计划：", json.dumps(new_schedule, indent=2, ensure_ascii=False))