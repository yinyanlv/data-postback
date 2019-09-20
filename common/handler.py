#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from common.store import mongo_store
from common.error import Error


class ResponseHandler:
    def __init__(self):
        pass

    def handle(self, response, original_data, filter_key, table_name):
        print('{}: {}'.format(response.status_code, response.url))
        if response.status_code == 200:
            res_data = response.json()
            status_code = res_data['status']
            """
                  200 成功
                  201 写入数据部分成功
                  202 写入数据全部失败
                  400 请求路径不正确
                  500 服务器未知错误
                  501 请求超时
                  900 业务逻辑错误
                  901 Token验证失败
                  902 Token失效
                  903 请求格式不对
              """
            if status_code == 200:
                pass
            elif status_code == 201:
                result = self.filter_data(original_data, res_data['response'], filter_key)
                mongo_store.save(table_name, result)
                Error(response.text, response.url).save()
            else:
                mongo_store.save(table_name, original_data)
                Error(response.text, response.url).save()
        else:
            mongo_store.save(table_name, original_data)
            Error(response.text, response.url).save()

    def filter_data(self, original_data, res_data, filter_key=''):
        result = []
        failed_list = []
        for item in res_data:
            if item['status'] != 'success' and filter_key != '':
                failed_list.append(item[filter_key])
        for item in original_data:
            if item[filter_key] in failed_list:
                result.append(item)
        return result


response_handler = ResponseHandler()
