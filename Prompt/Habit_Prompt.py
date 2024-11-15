habit_prompt = {
    "GAIA_ANSWER_EXTRACTOR_PROMPT": '''
    You are tasked as a habit and routine extractor. Your goal is to analyze the provided question and response, and extract key habits, decision-making rules, and time management practices in a structured format. Follow these directives:
    1. Identify and summarize the key routines or habits described, including their sequence and time allocation.  
    2. Extract decision-making rules, including conditions or factors influencing choices.  
    3. Account for exceptions or special conditions described in the response.  
    4. Return the habits and routines in a structured JSON format, adhering to the example below:

    Here is an examples to guide your extraction:
    **Example **:  
    **Question**: [
    {"Active": "Playing with cell phone", "Type": "Social media", "Start Time": "September 28, 2024 8:47 AM", "End Time": "", "Date": "2024/09/28"},
    {"Active": "Studying", "Type": "Study", "Start Time": "September 27, 2024 4:01 PM", "End Time": "September 27, 2024 5:20 PM", "Date": "2024/09/27"},
    {"Active": "Eating", "Type": "Routine", "Start Time": "September 27, 2024 12:44 PM", "End Time": "September 27, 2024 1:15 PM", "Date": "2024/09/27"}
    ]

    **Extracted Habits and Rules**:  
    ```json
    {
        "Habits": [
            {
                "Pattern": "Morning relaxation",
                "Description": "Often starts the day with a short period of relaxation, such as browsing social media."
            },
            {
                "Pattern": "Afternoon focus",
                "Description": "Usually engages in focused activities like studying during the afternoon, lasting for about 1-2 hours."
            },
            {
                "Pattern": "Midday meal breaks",
                "Description": "Takes regular meal breaks around noon, usually lasting 30 minutes to an hour."
            },
            {
                "Pattern": "Evening relaxation",
                "Description": "Ends the day with a longer relaxation period, often involving entertainment or social media."
            }
        ],
        "Behavioral Tendencies": [
            {
                "Observation": "Transitions from focused tasks to leisure activities",
                "Details": "After study or work sessions, often takes time to unwind with a relaxing activity."
            },
            {
                "Observation": "Prefers short breaks during midday",
                "Details": "Activities around noon are usually brief, often involving meals or light social media browsing."
            }
        ]
    }
    '''
}