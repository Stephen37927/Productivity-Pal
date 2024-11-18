from datetime import datetime
import subprocess


# 输出脚本执行的返回
def run_applescript(applescript):
    process = subprocess.Popen(['osascript', '-e', applescript], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        print("操作成功!")
        return output.decode().strip()
    else:
        print(f"操作失败: {error.decode()}")

def create_reminder_script(title, date, time):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%A, %B %d, %Y")
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

# 入参是开始日期和结束日期，输出是 已完成的提醒事项 。输出需要split(", ")处理
# 获取指定时间完成的提醒事项，举例 2020-11-01 00:00:00 至  2024-11-30 23:59:59 内完成的
def get_completed_reminders(start_time, end_time):
    start_time = datetime.strptime(start_time, "%Y-%m-%d").strftime("%Y-%m-%d 00:00:00")
    end_time = datetime.strptime(end_time, "%Y-%m-%d").strftime("%Y-%m-%d 23:59:59")
    
    applescript = f'''
    on get_completed_reminders_within()
        set theReminders to {{}}
        set startDate to date "{start_time}"
        set endDate to date "{end_time}"
        tell application "Reminders"
            repeat with r in (reminders whose completed is true)
                set completionDate to completion date of r
                if completionDate ≥ startDate and completionDate ≤ endDate then
                    set end of theReminders to name of r
                end if
            end repeat
        end tell
        return theReminders
    end get_completed_reminders_within

    get_completed_reminders_within()
    '''
    return applescript

# 获取当前过期未完成的提醒事项
def get_uncompleted_reminders():
    applescript = '''
    on get_overdue_incomplete_reminders()
        set theReminders to {}
        set currentDate to current date
        tell application "Reminders"
            repeat with r in (reminders whose completed is false)
                set dueDate to due date of r
                if dueDate is not missing value and dueDate < currentDate then
                    set end of theReminders to name of r
                end if
            end repeat
        end tell
        return theReminders
    end get_overdue_incomplete_reminders

    get_overdue_incomplete_reminders()
    '''
    return applescript

def get_calendar_events():
    script = """
    tell application "Calendar"
        set eventList to {}
        repeat with c in calendars
            set e to (events of c whose status is completed)
            repeat with i in e
                set end of eventList to summary of i
            end repeat
        end repeat
        return eventList
    end tell
    """
    process = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return process.stdout.strip().split(", ")




eventName = "会议"
eventDate = "2024-11-20"
eventStartTime = "10:00 AM"
eventEndTime = "11:00 AM"
reminder_script = create_reminder_script(eventName, eventDate, eventStartTime)
event_script = create_event_script(eventName, eventDate, eventStartTime, eventEndTime)
get_reminder_script=get_completed_reminders("2020-11-01", "2024-11-30")
get_uncompleted_reminders_script = get_uncompleted_reminders()
#run_applescript(reminder_script)
# run_applescript(event_script)
print(run_applescript(get_reminder_script).split(", "))
print(run_applescript(get_uncompleted_reminders_script).split(", "))