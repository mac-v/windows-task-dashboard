# Task Scheduler App


### Features:
1. Show the schedule of tasks for each day of the week (Monday - Sunday).
   - Display tasks across different hours: 8-9 AM, 9-10 AM, and so on, with their names.
2. Display today's schedule with statuses and possible error stack traces.
   - Send an email if one of report failed
3. Update the database with newly added, removed, or updated tasks.
   - Provide alerts about the results of the update.

## How to Link Objects Between Executed Task and Scheduled Task?
- The linking can be done based on static path of the .py file.

### DB structure

#### Table: tasks
- **id**: Name of task (PK)
- **status**: On/Off status
- **author**: Author of task
- **execution_schedule**: Schedule of task

#### Table: TasksExecutions
- **id**: Name of task (FK)
- **status**: Failed/Passed status
- **stack_trace**: Possible stack trace
- **date_of_execution**: (D M Y H M) date of execution 

#### Table: receivers
- **email**: (PK) 
- **name**: Name of receiver
- **active**: Is user active, if not do not send
