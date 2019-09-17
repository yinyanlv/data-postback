#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from common.config import conf
from common.utils import get_connection

host = conf.get('app.db', 'host')
port = conf.get('app.db', 'port')
username = conf.get('app.db', 'username')
password = conf.get('app.db', 'password')
database = conf.get('app.db', 'database')
driver = conf.get('app.db', 'driver')


app_conn = get_connection(driver, host, port, database, username, password)