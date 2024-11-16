import json
import pytest
from unittest.mock import MagicMock
from Habit_Prompt import habit_prompt
from doubao_client import DoubaoClient
from db_interface import HabitExtractor  # 替换为 HabitExtractor 的实际文件路径

@pytest.fixture
def mock_doubao_client():
    """
    Fixture to provide a mock DoubaoClient.
    """
    mock_client = MagicMock(spec=DoubaoClient)
    mock_client.chat.return_value = json.dumps({
        "Habits": [
            {
                "Pattern": "Morning Study",
                "Description": "Often studies during the morning hours."
            },
            {
                "Pattern": "Afternoon Relaxation",
                "Description": "Usually takes a short break in the afternoon for leisure activities."
            }
        ],
        "Behavioral Tendencies": [
            {
                "Observation": "Focus during study",
                "Details": "Prefers a quiet environment for studying."
            }
        ]
    })
    return mock_client

@pytest.fixture
def habit_extractor(mock_doubao_client):
    """
    Fixture to provide a HabitExtractor with a mock DoubaoClient.
    """
    return HabitExtractor(llm_client=mock_doubao_client)

def test_extract_habits(habit_extractor, mock_doubao_client):
    """
    Test the extract_habits method of HabitExtractor.
    """
    # 模拟输入任务数据
    tasks = [
        {"Active": "Studying", "Type": "Study", "Start Time": "2024-11-10 14:00", "End Time": "2024-11-10 15:30", "Date": "2024-11-10"},
        {"Active": "Eating", "Type": "Routine", "Start Time": "2024-11-11 12:00", "End Time": "2024-11-11 12:30", "Date": "2024-11-11"},
        {"Active": "Jogging", "Type": "Exercise", "Start Time": "2024-11-12 07:00", "End Time": "2024-11-12 07:30", "Date": "2024-11-12"}
    ]

    # 执行方法
    extracted_habits = habit_extractor.extract_habits(tasks)

    # 检查是否调用了 DoubaoClient 的 chat 方法
    mock_doubao_client.chat.assert_called_once()

    # 检查调用时的 prompt_input 是否正确
    expected_prompt_input = {
        "Habits_Input": tasks,
        "Prompt": habit_prompt["GAIA_ANSWER_EXTRACTOR_PROMPT"]
    }
    mock_doubao_client.chat.assert_called_with(
        endpoint_key="HABIT_EXTRACTION_ENPOINT",
        prompt=json.dumps(expected_prompt_input)
    )

    # 检查返回结果是否符合预期
    assert "Habits" in extracted_habits, "Habits key should be in the response"
    assert len(extracted_habits["Habits"]) > 0, "Habits should not be empty"
    assert extracted_habits["Habits"][0]["Pattern"] == "Morning Study", "First habit should match expected pattern"

    print("Test passed: HabitExtractor extract_habits works as expected.")

if __name__ == "__main__":
    pytest.main(["-q", __file__])