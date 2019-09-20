#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from datetime import datetime
from common.store import mongo_store


class Error:
    def __init__(self, message, url=''):
        self.url = url
        self.datetime = datetime.now()
        self.message = message

    def save(self):
        mongo_store.save_error(self.__dict__)
