import json
import subprocess
from datetime import datetime
from oscopilot.modules.schedule_maker.schedule_maker import ScheduleMaker


def run_applescript(applescript):
    """
    运行 AppleScript 并捕获输出或错误。
    """
    process = subprocess.Popen(['osascript', '-e', applescript], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        print(f"操作成功: {output.decode().strip()}")
    else:
        print(f"操作失败: {error.decode().strip()}")


def create_reminder_script(title, date, time):
    """
    创建提醒的 AppleScript。
    """
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    # formatted_date = date_obj.strftime("%A, %B %d, %Y")
    applescript = f'''
    on createReminder(reminderTitle, reminderDate, reminderTime)
        tell application "Reminders"
            set fullDateTime to reminderDate & " " & reminderTime
            set newReminder to make new reminder with properties {{name:reminderTitle, remind me date:date fullDateTime}}
        end tell
    end createReminder

    createReminder("{title}", "{date}", "{time}")
    '''
    return applescript


def create_event_script(event_title, event_date, event_start_time, event_end_time):
    """
    创建日历事件的 AppleScript。
    """
    date_obj = datetime.strptime(event_date, "%Y-%m-%d")
    # 获取年、月、日
    year = date_obj.strftime("%Y")
    month = date_obj.strftime("%m")
    day = date_obj.strftime("%d")
    applescript = f'''
    on createEvent(eventTitle, eventYear, eventMonth, eventDay, eventStartTime, eventEndTime)
        tell application "Calendar"
            tell calendar "Home"
                -- 设置开始日期
                set my_start_date to current date
                set year of my_start_date to {year} as integer
                set month of my_start_date to {month} as integer
                set day of my_start_date to {day} as integer

                -- 解析开始时间
                set hours to (text 1 thru 2 of eventStartTime) as integer
                set minutes to (text 4 thru 5 of eventStartTime) as integer
                set time of my_start_date to (hours * 3600 + minutes * 60)

                -- 设置结束日期
                set my_end_date to current date
                set year of my_end_date to {year} as integer
                set month of my_end_date to {month} as integer
                set day of my_end_date to {day} as integer

                -- 解析结束时间
                set hours to (text 1 thru 2 of eventEndTime) as integer
                set minutes to (text 4 thru 5 of eventEndTime) as integer
                set time of my_end_date to (hours * 3600 + minutes * 60)

                -- 创建事件
                make new event with properties {{summary:eventTitle, start date:my_start_date, end date:my_end_date}}
            end tell
        end tell
    end createEvent

    createEvent("{event_title}", "{year}", "{month}", "{day}", "{event_start_time}", "{event_end_time}")
    '''
    return applescript


def execute_schedule_with_applescript(schedule):
    """
    根据生成的计划，使用 AppleScript 创建日历事件和提醒。
    """
    try:
        # 遍历计划中的任务
        for task in schedule:
            title = task["Task"]
            date = task["Date"]
            start_time = task["StartTime"]
            end_time = task["EndTime"]

            # 创建提醒和事件的 AppleScript
            reminder_script = create_reminder_script(title, date, start_time)
            event_script = create_event_script(title, date, start_time, end_time)

            # 执行 AppleScript
            run_applescript(reminder_script)
            run_applescript(event_script)

    except Exception as e:
        print(f"执行计划时出错: {e}")


def main():
    schedule_maker = ScheduleMaker()
    deadline = "202411201200"
    deadline_name = "Cleaning Toilet"

    schedule_json = schedule_maker.create_schedule(deadline, deadline_name)

    # 将计划解析为 JSON 对象
    try:
        if not schedule_json:
            print("Received empty response.")
            return
        print(f"Raw response: {schedule_json}")
        schedule_json = schedule_json.strip()
        schedule = json.loads(schedule_json)
        print("生成的计划:", json.dumps(schedule, indent=2))

        execute_schedule_with_applescript(schedule)

    except json.JSONDecodeError as e:
        print(f"解析计划时出错: {e}")
        print(f"Invalid JSON content: {schedule_json}")


if __name__ == "__main__":
    main()