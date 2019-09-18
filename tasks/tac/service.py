#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from os import path
from tasks.tac.db import tac_cursor
from common.utils import get_day_time_range, read_text


class TacService:

    def __init__(self):
        self.question_sql = read_text(path.join(path.dirname(__file__), 'sqls/question.sql'))
        self.feedback_sql = read_text(path.join(path.dirname(__file__), 'sqls/feedback.sql'))
        self.repair_sql = read_text(path.join(path.dirname(__file__), 'sqls/repair.sql'))

    def get_feedback(self, timestamp):
        data = []
        day_time_range = get_day_time_range(timestamp)
        day_time_range = {
            'begin': '2019-03-16 00:00:00',
            'end': '2019-08-20 00:00:00'
        }
        print(day_time_range)
        tac_cursor.execute(self.feedback_sql, day_time_range)
        fields = [desc_row[0].lower() for desc_row in tac_cursor.description]
        print(fields)
        for row in tac_cursor:
            item = {}
            for i, field in enumerate(fields):
                item[field] = row[i]
            data.append(item)
        return data


tac_service = TacService()
