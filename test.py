from oscopilot.modules.habit_tracker.habit_tracker import HabitTracker
habit_tracker = HabitTracker()
logs = habit_tracker.fetch_recent_logs(7)
habit = habit_tracker.get_habit_from_logs()
print(habit)
# habit_tracker.save_habit(habit)



