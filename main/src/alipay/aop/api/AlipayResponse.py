# -*- coding: utf-8 -*-
'''
Created on 2017-12-20

@author: liuqun
'''
import json


class AlipayResponse(object):

    def __init__(self, response_str=None):
        if not response_str:
            self.code = ""
            self.msg = ""
            self.sub_code = ""
            self.sub_msg = ""
            self.response_str = ""
        else:
            self.response_str = response_str
            responseJson = json.loads(response_str)
            self.code = responseJson["code"]
            self.msg = responseJson["msg"]
            if responseJson["sub_code"]:
                self.sub_code = responseJson["sub_code"]
            if responseJson["sub_msg"]:
                self.sub_msg = responseJson["sub_msg"]

    def get_code(self):
        return self.code

    def get_msg(self):
        return self.msg

    def get_sub_code(self):
        return self.sub_code

    def get_sub_msg(self):
        return self.sub_msg

    def get_response_str(self):
        return self.response_str
