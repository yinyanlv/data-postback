#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from common.config import conf
from common.utils import get_connection

host = conf.get('tac.db', 'host')
port = conf.get('tac.db', 'port')
username = conf.get('tac.db', 'username')
password = conf.get('tac.db', 'password')
database = conf.get('tac.db', 'database')
driver = conf.get('tac.db', 'driver')

tac_conn = get_connection(driver, host, port, database, username, password)
tac_cursor = tac_conn.cursor()
