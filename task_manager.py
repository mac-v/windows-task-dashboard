import datetime

import win32com.client
import xmltodict
import pprint
import re


## Getting windows scheduled tasks and their's info
#### What should be achievied ?
## 1.get props from win32 of all tasks -> Load it to task object -> load object to ORM -> ORM insert
def get_python_file_name_from_bat(bat_file_path):
    if bat_file_path[-4:0] != ".bat":
        "Unknown - no bat file"
    else:
        with open(bat_file_path, 'r') as file:
            batch_content = file.read()
        pattern = r'(\b\w+\.py\b)'
        match = re.search(pattern, batch_content)
        return match.group()


def find_nested_dict_value(multi_dictionary, dict_key):
    ## Checking if given level of dictionary is found and it's keys are found
    if dict_key in multi_dictionary:
        return multi_dictionary[dict_key]
    else:
        # Some keys are are inner dictionares some not
        # so we look only at dicts
        for key, value in multi_dictionary.items():
            if isinstance(value, dict):
                ## value is our new dict to search
                result = find_nested_dict_value(value, dict_key)
                if result is not None:
                    return result


def get_schedule(xml_dict):
    def handle_logon_trigger(xml_dict):
        return {"schedule_type": "LogonTrigger"}

    def handle_time_trigger(xml_dict):
        time_trigger_interval = find_nested_dict_value(xml_dict, "Interval")
        execution_time = find_nested_dict_value(xml_dict, "StartBoundary")
        return {"schedule_type": "TimeTrigger",
                "time_trigger_interval": time_trigger_interval,
                "execution_time": execution_time}

    def handle_calendar_trigger(xml_dict):

        calendar_trigger_days = find_nested_dict_value(xml_dict, "DaysOfWeek")
        calendar_trigger_weeks_interval = find_nested_dict_value(xml_dict, "WeeksInterval")
        if isinstance(calendar_trigger_days, dict):
            calendar_trigger_days = ', '.join(str(key) for key in calendar_trigger_days.keys())

        execution_time = find_nested_dict_value(xml_dict, "StartBoundary")
        return {"schedule_type": "CalendarTrigger",
                "calendar_trigger_days": calendar_trigger_days,
                "calendar_trigger_weeks_interval": calendar_trigger_weeks_interval,
                "execution_time": execution_time}

    trigger_handlers = {
        "LogonTrigger": handle_logon_trigger,
        "TimeTrigger": handle_time_trigger,
        "CalendarTrigger": handle_calendar_trigger
    }

    for trigger_type, handler_func in trigger_handlers.items():
        if find_nested_dict_value(xml_dict, trigger_type):
            return handler_func(xml_dict)

    return {"type": "Unknown"}


class Task:

    def __init__(self, xml_dict):
        task_name = find_nested_dict_value(xml_dict, "URI")
        author = find_nested_dict_value(xml_dict, "Author")

        report_name = get_python_file_name_from_bat(find_nested_dict_value(xml_dict, "Command"))
        execution_schedule = get_schedule(xml_dict)
        self.task_name = task_name
        self.author = author
        self.report_name = report_name
        self.execution_schedule = execution_schedule

    def __str__(self):
        return (f"Task: {self.task_name}, Author: {self.author},"
                f" Report: {self.report_name}, Schedule: {self.execution_schedule}")

    def to_dict(self):
        execution_time = self.execution_schedule.get("execution_time")
        if execution_time != None:
            execution_time = datetime.datetime.strptime(execution_time, '%Y-%m-%dT%H:%M:%S')

        return {
            "task_name": self.task_name,
            "report_name": self.report_name,
            "author": self.author,
            "schedule_type": self.execution_schedule["schedule_type"],
            "time_trigger_interval": self.execution_schedule.get("time_trigger_interval"),
            "calendar_trigger_days": self.execution_schedule.get("calendar_trigger_days"),
            "calendar_trigger_weeks_interval": self.execution_schedule.get("calendar_trigger_weeks_interval"),
            "execution_time": execution_time
        }


def retrieve_windows_task():
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()

    folders = [scheduler.GetFolder("\\")]
    tasks_list = []
    while folders:
        folder = folders.pop(0)
        windows_tasks = folder.GetTasks(0)

        for windows_task in windows_tasks:
            xml_task = xmltodict.parse(windows_task.Xml)
            tasks_list.append(Task(xml_task))
            pprint.pprint(xml_task)
    for task in tasks_list:
        print(task)

    return tasks_list


retrieve_windows_task()
