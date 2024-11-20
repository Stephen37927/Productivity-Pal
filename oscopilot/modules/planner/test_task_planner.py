import unittest
from oscopilot.modules.planner.task_planner import TaskPlanner

class TestTaskPlanner(unittest.TestCase):
    def test_task_planner(self):
        task_planner = TaskPlanner()
        task_name = "Financial Fraud Presentation"
        task_description = "Prepare a presentation on financial fraud for the upcoming conference."
        tasks = task_planner.divide_task(task_name,task_description,"2024-11-30 23:59:59")  
        sche= task_planner.schedule_task(1,tasks,"2024-11-15 23:59:59","2024-11-30 23:59:59")
        task_planner.execute_schedule_with_applescript(sche)
        print("拆解的任务:\n",sche)
        

if __name__ == "__main__":
    unittest.main()

    