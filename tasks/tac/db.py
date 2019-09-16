#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from common.config import conf
from common.utils import get_connect

host = conf.get('tac.db', 'host')
port = conf.get('tac.db', 'port')
username = conf.get('tac.db', 'username')
password = conf.get('tac.db', 'password')
database = conf.get('tac.db', 'database')
driver = conf.get('tac.db', 'driver')

server = host if port == '' else host + ':' + port

tac_conn = get_connect(driver, server, database, username, password)
tac_cursor = tac_conn.cursor()
