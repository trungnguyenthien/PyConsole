from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import sys

def print_current_time():
    now = datetime.now()
    current_time = now.strftime("Now is %Y-%m-%d %H-%M-%S")
    print(current_time, flush=True)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(print_current_time, 'interval', seconds=5)
    scheduler.start()
