import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from database import DailyLogDatabase  # 确保类名与定义一致

class TestDailyLogDatabase(unittest.TestCase):
    def setUp(self):
        """
        设置测试环境，mock 数据库集合。
        """
        self.mock_collection = MagicMock()
        self.db = DailyLogDatabase("daily_logs")
        self.db.collection = self.mock_collection  # 替换数据库集合为 mock

    @patch("database.datetime")  # Mock datetime.now()
    def test_find_by_deadline(self, mock_datetime):
        """
        测试 find_by_deadline 函数是否正确返回符合条件的记录。
        """
        # 模拟当前时间
        mock_datetime.now.return_value = datetime(2024, 11, 15, 11, 30)  # 当前时间：2024-11-15 11:30
        mock_datetime.strptime.side_effect = datetime.strptime

        # 模拟数据库中的日志数据
        mock_data = [
            {"Name": "小丑牌", "Start Time": "202411151116", "End Time": "202411151243", "Type": "游戏"},  # 持续 27 分钟
            {"Name": "打球", "Start Time": "202411151200", "End Time": "202411151300", "Type": "运动"},  # 持续 60 分钟
            {"Name": "阅读", "Start Time": "202411151230", "End Time": "202411151330", "Type": "学习"},  # 持续 30 分钟
            {"Name": "散步", "Type": "休闲"}  # 缺少时间字段
        ]
        self.mock_collection.find.return_value = mock_data

        # 用户输入的截止日期
        deadline_input = "202411151200"  # 用户输入的截止日期为 2024-11-15 12:00

        # 调用函数
        results = self.db.find_by_deadline(deadline_input)

        # 验证结果是否符合预期
        # 打印结果
        if len(results) > 0:
            print("搜索结果:", results)
        else:
            print("没有找到符合条件的结果。")

        # 验证结果数量是否大于 0
        self.assertGreater(len(results), 0, "查询未返回任何结果。")


if __name__ == "__main__":
    unittest.main()