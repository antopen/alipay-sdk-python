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
        if not has_value(self.__configs, P_CHARSET):
            self.__configs[P_CHARSET] = "utf-8"
        else:
            self.__configs[P_CHARSET] = self.__configs[P_CHARSET].lower()
        if not has_value(self.__configs, P_TIMEOUT):
            self.__configs[P_TIMEOUT] = 15
        self.__configs[P_FORMAT] = "json"
        self.__configs[P_VERSION] = "1.0"
        self.__logger = logger

    def get_common_params(self, params):
        common_params = dict()
        common_params[P_TIMESTAMP] = params[P_TIMESTAMP]
        common_params[P_APP_ID] = self.__configs[P_APP_ID]
        common_params[P_METHOD] = params[P_METHOD]
        common_params[P_CHARSET] = self.__configs[P_CHARSET]
        common_params[P_FORMAT] = self.__configs[P_FORMAT]
        common_params[P_VERSION] = self.__configs[P_VERSION]
        common_params[P_SIGN_TYPE] = self.__configs[P_SIGN_TYPE]
        if has_value(self.__configs, P_ENCRYPT_TYPE):
            common_params[P_ENCRYPT_TYPE] = self.__configs[P_ENCRYPT_TYPE]
        if has_value(params, P_APP_AUTH_TOKEN):
            common_params[P_APP_AUTH_TOKEN] = params[P_APP_AUTH_TOKEN]
        if has_value(params, P_AUTH_TOKEN):
            common_params[P_AUTH_TOKEN] = params[P_AUTH_TOKEN]
        if has_value(params, P_NOTIFY_URL):
            common_params[P_NOTIFY_URL] = params[P_NOTIFY_URL]
        if has_value(params, P_RETURN_URL):
            common_params[P_RETURN_URL] = params[P_RETURN_URL]
        return common_params

    def remove_common_params(self, params):
        if not params:
            return
        for k in COMMON_PARAM_KEYS:
            if k in params:
                params.pop(k)

    def parse_response(self, response_str):
        m1 = PATTERN_RESPONSE_BEGIN.search(response_str)
        m2 = PATTERN_RESPONSE_SIGN_BEGIN.search(response_str)
        if (not m1) or (not m2):
            raise ResponseException('[' + THREAD_LOCAL.uuid + ']response shape maybe illegal. ' + response_str)
        sign_start_index = m2.start()
        sign_end_index = m2.end()
        while m2:
            m2 = PATTERN_RESPONSE_SIGN_BEGIN.search(response_str, pos=m2.end())
            if m2:
                sign_start_index = m2.start()
                sign_end_index = m2.end()

        response_content = response_str[m1.end() - 1:sign_start_index + 1]
        if PYTHON_VERSION_3:
            response_content = response_content.encode(self.__configs[P_CHARSET])
        sign = response_str[sign_end_index:response_str.find("\"", sign_end_index)]
        try:
            verify_res = verify_with_rsa(self.__configs[P_ALIPAY_PUBLIC_KEY], response_content, sign)
        except Exception as e:
            raise ResponseException('[' + THREAD_LOCAL.uuid + ']response sign verify failed. ' + str(e) + \
                                    ' ' + response_str)
        if not verify_res:
            raise ResponseException('[' + THREAD_LOCAL.uuid + ']response sign verify failed. ' + response_str)
        return response_content.decode(self.__configs[P_CHARSET])

    def build_form(self, url, params):
        form = "<form name=\"punchout_form\" method=\"post\" action=\""
        form += url
        form += "\">\n"
        if params:
            for k, v in params.items():
                if not v:
                    continue
                form += "<input type=\"hidden\" name=\""
                form += k
                form += "\" value=\""
                form += (json.dumps(v, ensure_ascii=False)).replace("\"", "&quot;")
                form += "\">\n"
        form += "<input type=\"submit\" value=\"立即支付\" style=\"display:none\" >\n"
        form += "</form>\n"
        form += "<script>document.forms[0].submit();</script>"
        return form

    def prepare(self, method, params):
        THREAD_LOCAL.logger = self.__logger

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params[P_TIMESTAMP] = timestamp
        params[P_METHOD] = method

        common_params = self.get_common_params(params)

        all_params = dict()
        all_params.update(params)
        all_params.update(common_params)
        sign_content = get_sign_content(all_params)
        sign_content_str = sign_content
        if PYTHON_VERSION_3:
            sign_content = sign_content.encode(self.__configs[P_CHARSET])
        try:
            if has_value(self.__configs, P_SIGN_TYPE) and self.__configs[P_SIGN_TYPE] == 'RSA2':
                sign = sign_with_rsa2(self.__configs[P_APP_PRIVATE_KEY], sign_content)
            else:
                sign = sign_with_rsa(self.__configs[P_APP_PRIVATE_KEY], sign_content)
        except Exception as e:
            raise RequestException('[' + THREAD_LOCAL.uuid + ']request sign failed. ' + str(e))
        if PYTHON_VERSION_3:
            sign = str(sign, encoding=self.__configs[P_CHARSET])

        common_params[P_SIGN] = sign

        query_string = url_encode(common_params, self.__configs[P_CHARSET])
        self.remove_common_params(params)

        log_url = self.__configs[P_SERVER_URL] + '?' + sign_content_str
        THREAD_LOCAL.logger.info('[' + THREAD_LOCAL.uuid + ']request:' + log_url)
        return query_string, params

    def after(self, response):
        if PYTHON_VERSION_3:
            response = response.decode(self.__configs[P_CHARSET])
        THREAD_LOCAL.logger.info('[' + THREAD_LOCAL.uuid + ']response:' + response)
        return self.parse_response(response)

    def execute(self, method, params):
        THREAD_LOCAL.uuid = str(uuid.uuid1())
        headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=' + self.__configs[P_CHARSET],
            "Cache-Control": "no-cache",
            "Connection": "Keep-Alive",
            "User-Agent": ALIPAY_SDK_PYTHON_VERSION,
            "log-uuid": THREAD_LOCAL.uuid,
        }

        query_string, params = self.prepare(method, params)

        response = post(self.__configs[P_SERVER_URL], query_string, headers, params, self.__configs[P_CHARSET],
                        self.__configs[P_TIMEOUT])

        return self.after(response)

    def multipart_execute(self, method, params, multipart_params):
        THREAD_LOCAL.uuid = str(uuid.uuid1())
        headers = {
            "Cache-Control": "no-cache",
            "Connection": "Keep-Alive",
            "User-Agent": ALIPAY_SDK_PYTHON_VERSION,
            "log-uuid": THREAD_LOCAL.uuid,
        }

        query_string, params = self.prepare(method, params)

        response = multipart_post(self.__configs[P_SERVER_URL], query_string, headers, params, multipart_params,
                                  self.__configs[P_CHARSET], self.__configs[P_TIMEOUT])

        return self.after(response)

    def page_execute(self, method, params, http_method="POST"):
        THREAD_LOCAL.uuid = str(uuid.uuid1())
        url = self.__configs[P_SERVER_URL]
        pos = url.find("?")
        if pos >= 0:
            url = url[0:pos]

        query_string, params = self.prepare(method, params)

        if http_method == "GET":
            return url + "?" + query_string + "&" + url_encode(params, self.__configs[P_CHARSET])
        else:
            return self.build_form(url + "?" + query_string, params)
