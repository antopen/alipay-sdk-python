# -*- coding: utf-8 -*-
'''
Created on 2017-12-20

@author: liuqun
'''
import datetime
import uuid

from alipay.aop.api.constant.ParamConstants import *
from alipay.aop.api.util.WebUtils import *
from alipay.aop.api.util.SignatureUtils import *
from alipay.aop.api.util.CommonUtils import *


class DefaultAlipayClient(object):

    def __init__(self, configs, logger):
        '''
        :param configs:
        {
            P_SERVER_URL: "https://openapi.alipay.com/gateway.do",
            P_APP_ID: "必填，应用ID",
            P_SIGN_TYPE: "必填，签名算法类型，目前支持RSA、RSA2",
            P_APP_PRIVATE_KEY: "必填，应用私钥",
            P_ALIPAY_PUBLIC_KEY: "必填，支付宝公钥,
            P_CHARSET: "可选，字符集编码，默认utf-8",
            P_ENCRYPT_TYPE: "可选，需要额外对称加密时，加密算法类型，目前只支持AES",
            P_ENCRYPT_KEY: "可选，需要额外对称加密时，加密密钥",
            P_TIMEOUT: 可选，请求超时时间，默认15s
        }
        '''
        self.__configs = configs
        if not hasValuableKey(self.__configs, P_CHARSET):
            self.__configs[P_CHARSET] = "utf-8"
        else:
            self.__configs[P_CHARSET] = self.__configs[P_CHARSET].lower()
        if not hasValuableKey(self.__configs, P_TIMEOUT):
            self.__configs[P_TIMEOUT] = 15
        self.__configs[P_FORMAT] = "json"
        self.__configs[P_VERSION] = "1.0"
        self.__logger = logger


    def getCommonParams(self, params):
        commonParams = dict()
        commonParams[P_TIMESTAMP] = params[P_TIMESTAMP]
        commonParams[P_APP_ID] = self.__configs[P_APP_ID]
        commonParams[P_METHOD] = params[P_METHOD]
        commonParams[P_CHARSET] = self.__configs[P_CHARSET]
        commonParams[P_FORMAT] = self.__configs[P_FORMAT]
        commonParams[P_VERSION] = self.__configs[P_VERSION]
        commonParams[P_SIGN_TYPE] = self.__configs[P_SIGN_TYPE]
        if hasValuableKey(self.__configs, P_ENCRYPT_TYPE):
            commonParams[P_ENCRYPT_TYPE] = self.__configs[P_ENCRYPT_TYPE]
        if hasValuableKey(params, P_APP_AUTH_TOKEN):
            commonParams[P_APP_AUTH_TOKEN] = params[P_APP_AUTH_TOKEN]
        if hasValuableKey(params, P_AUTH_TOKEN):
            commonParams[P_AUTH_TOKEN] = params[P_AUTH_TOKEN]
        if hasValuableKey(params, P_NOTIFY_URL):
            commonParams[P_NOTIFY_URL] = params[P_NOTIFY_URL]
        if hasValuableKey(params, P_RETURN_URL):
            commonParams[P_RETURN_URL] = params[P_RETURN_URL]
        return commonParams


    def removeCommonParams(self, params):
        if not params:
            return
        for k in COMMON_PARAM_KEYS:
            if k in params:
                params.pop(k)


    def parseResponse(self, responseStr):
        m1 = PATTERN_RESPONSE_BEGIN.search(responseStr)
        m2 = PATTERN_RESPONSE_SIGN_BEGIN.search(responseStr)
        if (not m1) or (not m2):
            raise ResponseException('[' + THREAD_LOCAL.uuid + ']response shape maybe illegal. ' + responseStr)
        signStartIndex = m2.start()
        signEndIndex = m2.end()
        while m2:
            m2 = PATTERN_RESPONSE_SIGN_BEGIN.search(responseStr, pos=m2.end())
            if m2:
                signStartIndex = m2.start()
                signEndIndex = m2.end()

        responseContent = responseStr[m1.end() - 1:signStartIndex + 1]
        if PYTHON_VERSION_3:
            responseContent = responseContent.encode(self.__configs[P_CHARSET])
        sign = responseStr[signEndIndex:responseStr.find("\"", signEndIndex)]
        try:
            verifyRes = verifyWithRSA(self.__configs[P_ALIPAY_PUBLIC_KEY], responseContent, sign)
        except Exception as e:
            raise ResponseException('[' + THREAD_LOCAL.uuid + ']response sign verify failed. ' + str(e) + \
                                    ' ' + responseStr)
        if not verifyRes:
            raise ResponseException('[' + THREAD_LOCAL.uuid + ']response sign verify failed. ' + responseStr)
        return responseContent.decode(self.__configs[P_CHARSET])


    def execute(self, method, params):
        THREAD_LOCAL.uuid = str(uuid.uuid1())
        THREAD_LOCAL.logger = self.__logger

        headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=' + self.__configs[P_CHARSET],
            "Cache-Control": "no-cache",
            "Connection": "Keep-Alive",
            "User-Agent": ALIPAY_SDK_PYTHON_VERSION,
            "log-uuid": THREAD_LOCAL.uuid,
        }

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params[P_TIMESTAMP] = timestamp
        params[P_METHOD] = method

        commonParams = self.getCommonParams(params)

        allParams = dict()
        allParams.update(params)
        allParams.update(commonParams)
        signContent = getSignContent(allParams)
        signContentStr = signContent
        if PYTHON_VERSION_3:
            signContent = signContent.encode(self.__configs[P_CHARSET])
        try:
            if hasValuableKey(self.__configs, P_SIGN_TYPE) and self.__configs[P_SIGN_TYPE] == 'RSA2':
                sign = signWithRSA2(self.__configs[P_APP_PRIVATE_KEY], signContent)
            else:
                sign = signWithRSA(self.__configs[P_APP_PRIVATE_KEY], signContent)
        except Exception as e:
            raise RequestException('[' + THREAD_LOCAL.uuid + ']request sign failed. ' + str(e))
        if PYTHON_VERSION_3:
            sign = str(sign, encoding=self.__configs[P_CHARSET])

        commonParams[P_SIGN] = sign

        queryString = urlencode(commonParams, self.__configs[P_CHARSET])
        self.removeCommonParams(params)

        logUrl = self.__configs[P_SERVER_URL] + '?' + signContentStr
        THREAD_LOCAL.logger.info('[' + THREAD_LOCAL.uuid + ']request:' + logUrl)

        response = post(self.__configs[P_SERVER_URL], queryString, headers, params, self.__configs[P_CHARSET],
                        self.__configs[P_TIMEOUT])
        if PYTHON_VERSION_3:
             response = response.decode(self.__configs[P_CHARSET])
        THREAD_LOCAL.logger.info('[' + THREAD_LOCAL.uuid + ']response:' + response)
        return self.parseResponse(response)



