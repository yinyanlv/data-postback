#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
from common.utils import gen_headers
from common.config import conf
from common.store import table_map
from common.handler import response_handler
from tasks.lac.service import lac_service

app_id = conf.get('lac', 'app_id')
secret_key = conf.get('lac', 'secret_key')
question_url = conf.get('lac', 'question_url')


class LacTask:
    def __init__(self):
        pass

    def send_question(self, timestamp):
        headers = gen_headers(app_id, secret_key, timestamp)
        data = lac_service.get_question(timestamp)
        res = requests.post(question_url, headers=headers, data={
            'data': data
        })
        response_handler.handle(res, data, 'autoId', table_map['lac'])


lac_task = LacTask()
