#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from common.config import conf
from common.utils import get_connection

host = conf.get('pac.db', 'host')
port = conf.get('pac.db', 'port')
username = conf.get('pac.db', 'username')
password = conf.get('pac.db', 'password')
database = conf.get('pac.db', 'database')
driver = conf.get('pac.db', 'driver')

pac_conn = get_connection(driver, host, port, database, username, password)
pac_cursor = pac_conn.cursor()
