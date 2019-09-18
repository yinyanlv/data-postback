#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from os import path
from tasks.tac.db import tac_cursor
from common.utils import get_day_time_range, read_text, rebuild_data


class TacService:

    def __init__(self):
        self.question_sql = read_text(path.join(path.dirname(__file__), 'sqls/question.sql'))
        self.feedback_sql = read_text(path.join(path.dirname(__file__), 'sqls/feedback.sql'))
        self.repair_sql = read_text(path.join(path.dirname(__file__), 'sqls/repair.sql'))

    def get_question(self, timestamp):
        data = self.get_data(timestamp, self.question_sql)
        return data

    def get_feedback(self, timestamp):
        data = self.get_data(timestamp, self.feedback_sql)
        return data

    def get_repair(self, timestamp):
        data = self.get_data(timestamp, self.repair_sql)
        return data

    def get_data(self, timestamp, sql):
        day_time_range = get_day_time_range(timestamp)
        tac_cursor.execute(sql, day_time_range)
        fields = [desc_row[0] for desc_row in tac_cursor.description]
        data = rebuild_data(tac_cursor, fields)
        return data

tac_service = TacService()
