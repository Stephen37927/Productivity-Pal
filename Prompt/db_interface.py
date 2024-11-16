import json
from unittest.mock import MagicMock
from doubao_client import DoubaoClient  # Import the working DoubaoClient
from Habit_Prompt import habit_prompt

# 模拟 MongoDB 操作
mock_find_recent_tasks = MagicMock(return_value=[
    {"Active": "Studying", "Type": "Study", "Start Time": "2024-11-10 14:00", "End Time": "2024-11-10 15:30", "Date": "2024-11-10"},
    {"Active": "Eating", "Type": "Routine", "Start Time": "2024-11-11 12:00", "End Time": "2024-11-11 12:30", "Date": "2024-11-11"},
    {"Active": "Jogging", "Type": "Exercise", "Start Time": "2024-11-12 07:00", "End Time": "2024-11-12 07:30", "Date": "2024-11-12"}
])

class HabitExtractor:
    def __init__(self, llm_client):
        """
        Initialize the HabitExtractor with an LLM client (DoubaoClient).
        """
        self.llm_client = llm_client

    def fetch_recent_tasks(self):
        """
        Simulate fetching tasks from the database.
        """
        tasks = mock_find_recent_tasks({})
        return tasks

    def extract_habits(self, tasks):
        """
        Use the LLM client to extract habits from the provided tasks.
        """
        # Construct the prompt input
        prompt_input = {
            "Habits_Input": tasks,
            "Prompt": habit_prompt["GAIA_ANSWER_EXTRACTOR_PROMPT"]
        }
        print("DEBUG: Prompt Input:", json.dumps(prompt_input, indent=4))
        # Call the DoubaoClient's chat method
        try:
            response = self.llm_client.chat(
                endpoint_key="HABIT_EXTRACTION_ENPOINT",  # Use hardcoded endpoint
                prompt=json.dumps(prompt_input)  # Serialize prompt to JSON
            )
            print("DEBUG: Raw Response from Doubao:", response)
            return json.loads(response)  # Parse the JSON response
        except json.JSONDecodeError as e:
            print(f"Error decoding response JSON: {e}")
            return None
        except Exception as e:
            print(f"Error in extracting habits: {e}")
            return None