#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from common.config import conf
from common.utils import get_connection

host = conf.get('lac.db', 'host')
port = conf.get('lac.db', 'port')
username = conf.get('lac.db', 'username')
password = conf.get('lac.db', 'password')
database = conf.get('lac.db', 'database')
driver = conf.get('lac.db', 'driver')

lac_conn = get_connection(driver, host, port, database, username, password)
lac_cursor = lac_conn.cursor()
