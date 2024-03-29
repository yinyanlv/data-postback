#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from common.config import conf
from common.utils import current_milli_time, get_error_str
from common.error import Error
from tasks.tac.task import tac_task
from tasks.pac.task import pac_task
from tasks.lac.task import lac_task


def job():
    print('{}: 开始执行任务'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    timestamp = current_milli_time()
    try:
        tac_task.send_question(timestamp)
        tac_task.send_feedback(timestamp)
        tac_task.send_repair(timestamp)
        pac_task.send_question(timestamp)
        lac_task.send_question(timestamp)
        print('{}: 执行任务成功'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    except Exception as e:
        error_str = get_error_str()
        Error(error_str).save()
        print('{}: 执行任务失败'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        print('Error:', e)


def main():
    scheduler = BlockingScheduler()
    # 每天24:00:00触发
    scheduler.add_job(job, 'cron', day_of_week='0-6', hour=0, minute=0, second=0)
    app_name = conf.get('app', 'name')
    print(app_name + ' is running!')
    scheduler.start()


if __name__ == '__main__':
    main()
