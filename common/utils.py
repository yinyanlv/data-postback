#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
import time
import traceback
import sys
from datetime import datetime
import hashlib
import pyodbc
import cx_Oracle
from pymongo import MongoClient


current_milli_time = lambda: int(round(time.time() * 1000))


def lower_first_letter(words):
    return words[0].lower() + words[1:]


def gen_md5(text):
    md5 = hashlib.md5(text.encode(encoding='utf-8'))
    return md5.hexdigest()


def get_error_str():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return str(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))


def gen_headers(app_id, secret_key, timestamp):
    headers = {
        'Content-Type': 'application/json',
        'AppId': app_id,
        'Token': gen_md5(app_id + str(timestamp) + secret_key),
        'Times': str(timestamp)
    }
    return headers


def datetime_handler(x):
    if isinstance(x, datetime):
        dt, _, _ = x.isoformat().partition('.')
        return dt
    raise TypeError("Unknown type")


def get_post_json_data(data):
    return json.dumps({
        'data': data
    }, default=datetime_handler)


def get_connection(driver, host, port, database, username, password):
    server = host if port == '' else host + ':' + port
    if driver == 'Oracle':
        conn_str = '{2}/{3}@{0}/{1}'.format(server, database, username, password)
        print('{} connect string: {}'.format(driver, conn_str))
        conn = cx_Oracle.connect(conn_str)
        return conn
    elif 'SQL Server' in driver:
        server = host if port == '' else host + ',' + port
        conn_str = 'DRIVER={{{0}}};SERVER={1};DATABASE={2};UID={3};PWD={4}'.format(driver, server, database, username,
                                                                                   password)
        print('{} connect string: {}'.format(driver, conn_str))
        conn = pyodbc.connect(conn_str)
        return conn
    elif driver == 'MongoDb':
        if username == '' or password == '':
            conn_str = 'mongodb://{0}/'.format(server)
        else:
            conn_str = 'mongodb://{1}:{2}@{0}/'.format(server, username, password)
        print('{} connect string: {}'.format(driver, conn_str))
        conn = MongoClient(conn_str)
        return conn
    else:
        return None


def get_day_time_range(timestamp):
    # 减去10分钟，避免24:00:00这种时间边界问题
    temp = (timestamp - 1000 * 60 * 10) // 1000
    day = datetime.fromtimestamp(temp).strftime('%Y-%m-%d')
    return {
        'begin': '{} 00:00:00'.format(day),
        'end': '{} 23:59:59'.format(day)
    }


def read_text(file_path):
    fd = open(file_path, mode='r', encoding='utf-8')
    result = fd.read().encode('utf-8')
    fd.close()
    return result


def rebuild_data(cursor, fields):
    data = []
    for row in cursor:
        item = {}
        for i, field in enumerate(fields):
            item[field] = row[i]
        data.append(item)
    return data
