import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from oscopilot import BaseModule
from oscopilot.prompts.taskplan_pt import taskPlannerPrompt
from oscopilot.utils.database import DailyLogDatabase
from oscopilot.modules.habit_tracker.habit_tracker import HabitTracker
from oscopilot.utils.utils import send_chat_prompts
import re
from add_events import AppleScript


load_dotenv(override=True)
MODEL_NAME = os.getenv('CALENDAR_PLAN_ENDPOINT')

class TaskPlanner(BaseModule):
    def __init__(self):
        super().__init__()
        self.habit_tracker = HabitTracker()
        self.prompt = taskPlannerPrompt["planning_prompt"]
        self.appleScript=AppleScript()

    # 返回一个字典，key是任务名称，value是预计任务耗时
    # 举例 {'Financial Fraud Presentation - Research': '10 hours', 'Financial Fraud Presentation - Outline Creation': '3 hours'}
    def divide_task(self,task_name,description,deadline):
        try:
            sys_prompt = self.prompt['_SYSTEM_TASK_DECOMPOSE_PROMPT']
            user_prompt = self.prompt['_USER_TASK_DECOMPOSE_PROMPT'].format(
                task=task_name,
                description=description,
                deadline=deadline
            )
            response = send_chat_prompts(sys_prompt, user_prompt, self.llm)
            task_list = json.loads(response)
            task_duration_dict = {item['Task']: item['Duration'] for item in task_list}
            return task_duration_dict
        except Exception as e:
            print(f"Error creating schedule: {e}")
            return None
    
    def schedule_task(self,user_id,task_dict,deadline):
        try:
            # Step1: 获取日历中deadline前存在的事件
            events=self.appleScript.get_calendar_events(deadline)
            
            # Step2: 获取用户最近7天的习惯
            habits=[]
            for key in task_dict:
                habit=self.habit_tracker.get_habit_from_logs(user_id,days=7, top_k=5)
            habits.append(habit)

            # Step3: 构建提示内容
            sys_prompt = self.prompt['_SYSTEM_TASK_SCHEDULE_PROMPT']
            user_prompt = self.prompt['_USER_TASK_SCHEDULE_PROMPT'].format(
                habits=habits,
                tasks=task_dict,
                existed_events=events,
                deadline=deadline
            )
            response = send_chat_prompts(sys_prompt, user_prompt, self.llm)
            return response
        except Exception as e:
            print(f"Error creating schedule: {e}")
            return None

if __name__ == '__main__':
    task_planner = TaskPlanner()
    task_name = "Financial Fraud Presentation"
    task_description = "Prepare a presentation on financial fraud for the upcoming conference."
    tasks= task_planner.divide_task(task_name,task_description,"2024-11-30 23:59:59")  
    print("拆解的任务:\n",tasks)