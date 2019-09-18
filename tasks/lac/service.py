#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from os import path
from tasks.lac.db import lac_cursor
from common.utils import get_day_time_range, read_text, rebuild_data, lower_first_letter


class LacService:

    def __init__(self):
        self.question_sql = read_text(path.join(path.dirname(__file__), 'sqls/question.sql'))

    def get_question(self, timestamp):
        day_time_range = get_day_time_range(timestamp)
        lac_cursor.execute(self.question_sql, [day_time_range['begin'], day_time_range['end']])
        fields = [lower_first_letter(desc_row[0]) for desc_row in lac_cursor.description]
        data = rebuild_data(lac_cursor, fields)
        return data


lac_service = LacService()
