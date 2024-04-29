from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from .log import log

def print_current_time():
    now = datetime.now()
    current_time = now.strftime("Now is %Y-%m-%d %H:%M:%S")
    log({"colunm": 1, "current_time": current_time})

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(print_current_time, 'interval', seconds=5)
    scheduler.start()
