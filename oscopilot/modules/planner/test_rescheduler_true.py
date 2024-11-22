import unittest
from datetime import datetime
from oscopilot.modules.schedule_maker.schedule_maker import Rescheduler


class TestRescheduler(unittest.TestCase):
    def setUp(self):
        """
        初始化测试环境，确保数据库连接和调度器实例可用。
        """
        self.user_id = 1  # 使用测试用户 ID
        self.reschedule_time = "2024-11-20 10:00"
        self.start_time = datetime.strptime("2024-11-17 00:00", "%Y-%m-%d %H:%M")
        self.deadline = datetime.strptime("2024-11-20 23:59", "%Y-%m-%d %H:%M")
        self.rescheduler = Rescheduler(self.user_id, self.reschedule_time, None)

    def tearDown(self):
        """
        测试完成后关闭数据库连接。
        """
        if hasattr(self.rescheduler.daily_log_db, "client"):
            self.rescheduler.daily_log_db.client.close()
        if hasattr(self.rescheduler.deadline_db, "client"):
            self.rescheduler.deadline_db.client.close()

    def test_get_tasks_to_reschedule(self):
        """
        测试从数据库中获取需要重新调度的任务。
        """
        tasks = self.rescheduler.get_tasks_to_reschedule()
        print("获取的任务:\n", tasks)
        self.assertGreater(len(tasks), 0, "任务列表不应为空")

    def test_get_recent_logs(self):
        """
        测试从数据库中获取最近一周的日志。
        """
        logs = self.rescheduler.get_recent_logs()
        print("获取的日志:\n", logs)
        self.assertGreater(len(logs), 0, "日志列表不应为空")

    def test_get_user_habits(self):
        """
        测试从用户日志中提取习惯。
        """
        tasks = self.rescheduler.get_tasks_to_reschedule()
        habits = self.rescheduler.get_user_habits(tasks)
        print("提取的用户习惯:\n", habits)
        self.assertGreater(len(habits), 0, "习惯列表不应为空")

    def test_reschedule_tasks(self):
        """
        测试使用真实数据生成调度计划。
        """
        tasks = self.rescheduler.get_tasks_to_reschedule()
        logs = self.rescheduler.get_recent_logs()
        habits = self.rescheduler.get_user_habits(tasks)

        schedule = self.rescheduler.reschedule_tasks(tasks, logs, habits, self.start_time, self.deadline)
        print("生成的任务计划:\n", schedule)
        self.assertIsNotNone(schedule, "调度计划不应为 None")
        self.assertGreater(len(schedule), 0, "调度计划应包含至少一个任务")


if __name__ == "__main__":
    unittest.main()