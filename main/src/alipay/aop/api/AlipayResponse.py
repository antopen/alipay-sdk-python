# -*- coding: utf-8 -*-
'''
Created on 2017-12-20

@author: liuqun
'''
import json


class AlipayResponse(object):

    def __init__(self, responseStr=None):
        if not responseStr:
            self.code = ""
            self.msg = ""
            self.sub_code = ""
            self.sub_msg = ""
            self.responseStr = ""
        else:
            self.responseStr = responseStr
            responseJson = json.loads(responseStr)
            self.code = responseJson["code"]
            self.msg = responseJson["msg"]
            if responseJson["sub_code"]:
                self.sub_code = responseJson["sub_code"]
            if responseJson["sub_msg"]:
                self.sub_msg = responseJson["sub_msg"]

    def getCode(self):
        return self.code

    def getMsg(self):
        return self.msg

    def getSubCode(self):
        return self.sub_code

    def getSubMsg(self):
        return self.sub_msg

    def getResponseStr(self):
        return self.responseStr
