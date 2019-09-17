#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from datetime import datetime
from common.store import mongo_store


class Error:
    def __init__(self, msg):
        self.datetime = datetime.now()
        self.error = msg

    def save(self):
        mongo_store.save_error({
            'datetime': self.datetime,
            'error': self.error
        })
