#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
from common.utils import gen_headers, get_post_json_data
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
    def send_question(self, timestamp):
        data = tac_service.get_question(timestamp)
        if len(data) == 0:
            print('TAC技术求援未发现数据')
            return
        headers = gen_headers(app_id, secret_key, timestamp)
        res = requests.post(question_url, headers=headers, data=get_post_json_data(data))
        response_handler.handle(res, data, 'helpCodeId', table_map['tac_question'])

    # 发送信息反馈
    def send_feedback(self, timestamp):
        data = tac_service.get_feedback(timestamp)
        if len(data) == 0:
            print('TAC信息反馈未发现数据')
            return
        headers = gen_headers(app_id, secret_key, timestamp)
        res = requests.post(feedback_url, headers=headers, data=get_post_json_data(data))
        response_handler.handle(res, data, 'tisId', table_map['tac_feedback'])

    # 发送维修通讯案例
    def send_repair(self, timestamp):
        data = tac_service.get_repair(timestamp)
        if len(data) == 0:
            print('TAC维修通讯案例未发现数据')
            return
        headers = gen_headers(app_id, secret_key, timestamp)
        res = requests.post(repair_url, headers=headers, data=get_post_json_data(data))
        response_handler.handle(res, data, 'tisMid', table_map['tac_repair'])


tac_task = TacTask()
