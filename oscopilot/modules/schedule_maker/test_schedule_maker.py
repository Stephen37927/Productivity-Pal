import unittest
from oscopilot.modules.schedule_maker.schedule_maker import ScheduleMaker

class TestScheduleMakerIntegration(unittest.TestCase):
    def test_create_schedule_real(self):
        """
        测试 create_schedule 方法的实际生成逻辑。
        """
        # 实例化 ScheduleMaker
        schedule_maker = ScheduleMaker()

        # 输入一个实际的 deadline
        deadline = "202411201200"

        # 调用 create_schedule 方法
        schedule = schedule_maker.create_schedule(deadline)

        # 打印生成的计划
        print("Generated Schedule:", schedule)

        # 验证 schedule 是否生成
        self.assertIsNotNone(schedule)
        self.assertIn("Task", schedule)  # 你可以根据期望的结果格式添加更多断言

if __name__ == "__main__":
    unittest.main()