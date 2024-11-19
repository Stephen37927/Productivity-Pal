from oscopilot.modules.habit_tracker.habit_tracker import HabitTracker

habit_tracker = HabitTracker()
# logs = habit_tracker.fetch_recent_logs(1, 10, -1, "study")
# print(logs)
habit = habit_tracker.get_habit_from_logs(user_id=1, days=-1, task="coding", top_k=20, )
print(habit)
# habit_tracker.save_habit(habit)



