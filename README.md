# Task Scheduler App


### Features:
1. Show the schedule of tasks for each day of the week (Monday - Sunday).
   - Display tasks across different hours: 8-9 AM, 9-10 AM, and so on, with their names.
2. Display today's failed reports with stack trace.
   - Send an email if one of report failed with link to specific stack trace
3. Update the database with newly added, removed, or updated tasks.
   - Provide alerts about the results of the update.
4. Manage list of e-mail receivers
   - add
   - remove
   - disable/enable

## How to Link Objects Between Executed Task and Scheduled Task?
- The linking can be done based on static path of the .py file.

## How to send e-mail ?
- Trigger on creation row within failed tasks table
- 
### DB structure

#### Table: tasks
- **id**: Id of task (PK, AUTO)
- **task_name**: Name of the scheduled tasks
- **report_name**: Name of report that is executed by task
- **author**: Creator of windows task
- **schedule_type**: Schedule type (Calendar/Time/Logon Trigger)
- **time_trigger_interval**: Interval of 
- **calendar_trigger_days**: Author of task
- **calendar_trigger_weeks_interval**: Schedule of task
- **execution_time**: Schedule of task

#### Table: tasks_execution_failures
- **id**: Id of task (FK)
- **task_name**: Name of the scheduled tasks
- **report_name**: Name of report that is executed by task
- **stack_trace**: Possible stack trace
- **date_of_execution**: (D M Y H M) date of execution 

#### Table: receivers
- **email**: (PK) 
- **name**: Name of receiver
- **active**: Is user active, if not do not send
