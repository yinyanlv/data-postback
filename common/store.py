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
table_map = {
    'error': conf.get('app.db', 'error_table'),
    'tac_question': 'tac_question',
    'tac_feedback': 'tac_feedback',
    'tac_repair': 'tac_repair',
    'pac': 'pac',
    'lac': 'lac'
}


class MongoStore:

    app_conn = get_connection(driver, host, port, database, username, password)
    db = app_conn[database]

    def __init__(self):
        self.coll_map = {
            table_map['error']: self.create_collection(table_map['error']),
            table_map['tac_question']: self.create_collection(table_map['tac_question']),
            table_map['tac_feedback']: self.create_collection(table_map['tac_feedback']),
            table_map['tac_repair']: self.create_collection(table_map['tac_repair']),
            table_map['pac']: self.create_collection(table_map['pac']),
            table_map['lac']: self.create_collection(table_map['lac']),
        }
        self.error_table = self.coll_map[table_map['error']]

    def is_collection_exists(self, coll_name):
        if coll_name in self.db.list_collection_names():
            return True
        else:
            return False

    def create_collection(self, coll_name):
        if self.is_collection_exists(coll_name):
            coll = self.db.get_collection(coll_name)
        else:
            coll = self.db.create_collection(coll_name)
        return coll

    def save(self, coll_name, data):
        coll = self.coll_map.get(coll_name)
        if coll:
            if len(data) != 0:
                print(data)
                _result = coll.insert_many(data)
        else:
            print('Can not find collection {} in mongodb!', coll_name)

    def save_error(self, error):
        _result = self.error_table.insert_one(error)


mongo_store = MongoStore()
