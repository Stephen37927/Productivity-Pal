habit_prompt = {
    "SYSTEM_PROMPT": '''
    You are tasked as a habit and routine extractor. Your goal is to analyze the provided question and response, and extract key habits, decision-making rules, and time management practices in a structured format. Follow these directives:
    1. Identify and summarize the key routines or habits described, including their sequence and time allocation.  
    2. Extract decision-making rules, including conditions or factors influencing choices.  
    3. Account for exceptions or special conditions described in the response.  
    4. Return the habits and routines in a structured JSON format.
    ''',
    "USER_PROMPT": '''
    Here is an example:
    **Activities**:
    1. Active: 玩手机; Type: 社交媒体; Start Time: 2024-09-28 8:47; Date: 2024-09-28;
    2. Active: 学习; Type: 学习; Start Time: 2024-09-27 16:01; End Time: 2024-09-27 17:20; Date: 2024-09-27;
    3. Active: 吃饭; Type: 日常, Start Time: 2024-09-27 12:44; End Time: 2024-09-27 13:15, Date: 2024-09-27;
    **Answer**:
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
