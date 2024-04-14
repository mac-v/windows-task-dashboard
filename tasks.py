import win32com.client
import xmltodict
import pprint

## Getting windows scheduled tasks and their's info


scheduler = win32com.client.Dispatch('Schedule.Service')
scheduler.Connect()

folders = [scheduler.GetFolder("\\")]
xml_tasks = []
# Task created locally with name test_1 to see particular info about user-created task
test1_task = ""
while folders:
    folder = folders.pop(0)
    tasks = folder.GetTasks(0)

    for task in tasks:
        # print("Task name:", task.Name)
        # print("Path to task:", task.Path)
        # print("Status:", task.State)
        # print(task.Xml)
        if task.Name == "test1":
            ## After invoking all available methods and props, founded wanted prop - .xml
            ## It gives info about task (triggers gives info about date of runs)

            test1_task = task.Xml
        xml_tasks.append(task.Xml)

# print(xml_tasks[0])
xml_dict = xmltodict.parse(test1_task)
pprint.pprint(xml_dict)
