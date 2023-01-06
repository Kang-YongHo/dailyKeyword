from apscheduler.schedulers.background import BackgroundScheduler
from .forms import *


def start():
    scheduler = BackgroundScheduler(timezone='Asia/Seoul')
    scheduler.start()

    scheduler.add_job(db_update, 'cron', hour='23', id="db_update")

