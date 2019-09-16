#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from tasks.tac.db import tac_cursor


class TacService:
    def __init__(self):
        pass


    def get_feedback(self, timestamp):
        data = []
        sql = '''
            SELECT ID AS TIS_ID, SUBMIT_DATE AS FEEDBACK_TIME FROM T_FEEDBACK
            WHERE CREATED_DATE 
            BETWEEN 
                TO_DATE(:1,'yyyy-mm-dd hh24:mi:ss') 
                AND 
                TO_DATE(:2,'yyyy-mm-dd hh24:mi:ss')
        '''
        tac_cursor.execute(sql, ('2019-08-16 00:00:00', '2019-08-19 00:00:00'))
        for row in tac_cursor:
            item = {}
            item['tisId'] = row[0]
            item['feedbackTime'] = row[1]
            data.append(item)
        return data

tac_service = TacService()