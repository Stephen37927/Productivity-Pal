from datetime import datetime
import subprocess

def run_applescript(applescript):
    process = subprocess.Popen(['osascript', '-e', applescript], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        print("操作成功!")
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

    createReminder("{title}", "{formatted_date}", "{time}")
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

eventName = "会议"
eventDate = "2024-11-20"
eventStartTime = "10:00 AM"
eventEndTime = "11:00 AM"
reminder_script = create_reminder_script(eventName, eventDate, eventStartTime.split(' ')[0])
event_script = create_event_script(eventName, eventDate, eventStartTime, eventEndTime)
run_applescript(reminder_script)
run_applescript(event_script)
