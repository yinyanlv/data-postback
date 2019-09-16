#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import configparser

# 三种模式：dev，test，prod
APP_MODE = os.getenv('APP_MODE')

conf = configparser.ConfigParser()


def init_conf():
    if APP_MODE == 'test':
        path = get_file_path('test.conf')
    elif APP_MODE == 'prod':
        path = get_file_path('prod.conf')
    else:
        path = get_file_path('dev.conf')
    conf.read(path)


def get_file_path(filename):
    return os.path.abspath(os.path.join(os.getcwd(), 'conf', filename))


init_conf()
