#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
from common.utils import gen_headers, get_post_json_data
from common.config import conf
from common.store import table_map
from common.handler import response_handler
from tasks.pac.service import pac_service

app_id = conf.get('pac', 'app_id')
secret_key = conf.get('pac', 'secret_key')
question_url = conf.get('pac', 'question_url')


class PacTask:
    def __init__(self):
        pass

    def send_question(self, timestamp):
        data = pac_service.get_question(timestamp)
        if len(data) == 0:
            print('PAC未发现数据')
            return
        headers = gen_headers(app_id, secret_key, timestamp)
        res = requests.post(question_url, headers=headers, data=get_post_json_data(data))
        response_handler.handle(res, data, 'autoId', table_map['pac'])


pac_task = PacTask()
