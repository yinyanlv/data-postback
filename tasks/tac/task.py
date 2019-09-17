#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
from common.utils import gen_headers
from common.config import conf
from common.store import table_map
from common.handler import response_handler
from tasks.tac.service import tac_service

app_id = conf.get('tac', 'app_id')
secret_key = conf.get('tac', 'secret_key')
question_url = conf.get('tac', 'question_url')
feedback_url = conf.get('tac', 'feedback_url')
repair_url = conf.get('tac', 'repair_url')


class TacTask:
    def __init__(self):
        pass

    # 发送技术求援
    def send_question(self):
        pass

    # 发送信息反馈
    def send_feedback(self, timestamp):
        headers = gen_headers(app_id, secret_key, timestamp)
        data = tac_service.get_feedback(timestamp)
        res = requests.post(feedback_url, headers=headers, data={
            'data': data
        })
        response_handler.handle(res, data, '', table_map['tac_feedback'])

    # 发送维修通讯案例
    def send_repair_bulletin(self):
        pass


tac_task = TacTask()
