import os
import unittest
from unittest.mock import patch, MagicMock
from oscopilot.modules.base_module import BaseModule

class TestBaseModule(unittest.TestCase):

    @patch.dict(os.environ, {"WORKING_DIR": "/Users/dingdingdingdingding/Desktop/HKU/sem1/NLP/Project/Productivity-Pal/working_dir"})
    def setUp(self):
        """
        Sets up the testing environment by configuring the WORKING_DIR environment variable
        and initializing the BaseModule.
        """
        self.module = BaseModule()  # 使用 BaseModule 的默认构造函数

    def test_extract_information(self):
        message = "[BEGIN]Task 1[END] and [BEGIN]Task 2[END]"
        result = self.module.extract_information(message, "[BEGIN]", "[END]")
        expected = ["Task 1", "Task 2"]
        self.assertEqual(result, expected)

    def test_extract_json_from_string(self):
        text = """```json
        {
            "task": "example",
            "status": "complete"
        }
        ```"""
        result = self.module.extract_json_from_string(text)
        expected = {
            "task": "example",
            "status": "complete"
        }
        self.assertEqual(result, expected)

    def test_extract_list_from_string(self):
        text = "1. Task A\n2. Task B\n3. Task C"
        result = self.module.extract_list_from_string(text)
        expected = ["Task A", "Task B", "Task C"]  # 修改期望值
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()