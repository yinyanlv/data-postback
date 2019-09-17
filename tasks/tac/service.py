#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from tasks.tac.db import tac_cursor
from common.utils import get_day_time_range


class TacService:
    def __init__(self):
        pass

    feedback_sql = '''
        SELECT ID AS TIS_ID, SUBMIT_DATE AS FEEDBACK_TIME FROM T_FEEDBACK
        WHERE CREATED_DATE 
        BETWEEN 
            TO_DATE(:begin,'yyyy-mm-dd hh24:mi:ss') 
            AND 
            TO_DATE(:end,'yyyy-mm-dd hh24:mi:ss')
    '''

    def get_feedback(self, timestamp):
        data = []
        day_time_range = get_day_time_range(timestamp)
        tac_cursor.execute(self.feedback_sql, day_time_range)
        for row in tac_cursor:
            item = {'tisId': row[0], 'feedbackTime': row[1]}
            data.append(item)
        return data


tac_service = TacService()
