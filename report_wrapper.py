import traceback
import sys
from datetime import datetime
import time

# Wrapper that will be used as environment when running .py files (reports)

def send_email(TO, link):
    # TO DO
    pass


def get_current_date():
    return datetime.now().strftime("%d-%m-%Y %H:%M")


def save_report(today, executed, traceback_val, report_path, exec_time):
    # TO DO
    pass


def run_report(function_to_invoke):
    today_date = datetime.now().strftime("%d-%m-%Y %H:%M")
    start_time = time.time()
    report_executed_successfully = True
    traceback_value = None
    path_to_report = sys.argv[0]
    try:
        function_to_invoke()
    except Exception as e:
        traceback_value = traceback.format_exc()
        print("Error: ", e)
        print("Traceback: ", traceback_value)
        report_executed_successfully = False
    finally:
        end_time = time.time()
        exec_time = end_time - start_time
        # save_report()
        print(f'''Today date: {today_date},
              -----------------------
              Report executed successfully?: {report_executed_successfully},
              ------------------------
              Traceback:{traceback_value},
              ------------------------
              Report path: {path_to_report}
              ------------------------
              Exec time: {exec_time}
              ------------------------
              ''')
