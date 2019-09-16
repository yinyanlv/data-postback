#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import time
import hashlib
import pyodbc
import cx_Oracle

current_milli_time = lambda: int(round(time.time() * 1000))


def gen_md5(str):
    md5 = hashlib.md5(str.encode(encoding='utf-8'))
    return md5.hexdigest()


def gen_headers(app_id, secret_key, timestamp):
    headers = {
        'AppId': app_id,
        'Token': gen_md5(app_id + str(timestamp) + secret_key),
        'Times': str(timestamp)
    }
    return headers


def get_connect(driver, server, database, username, password):
    if driver == 'Oracle':
        conn_str = '{3}/{4}@{1}/{2}'.format(driver, server, database, username, password)
        print('{} connect string: {}'.format(driver, conn_str))
        conn = cx_Oracle.connect(conn_str)
        return conn
    elif driver == 'SQL Server':
        conn_str = 'DRIVER={{{0}}};SERVER={1};DATABASE={2};UID={3};PWD={4}'.format(driver, server, database, username, password)
        print('{} connect string: {}'.format(driver, conn_str))
        conn = pyodbc.connect(conn_str)
        return conn
    else:
        return None
