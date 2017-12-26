# -*- coding: gbk -*-
'''
Created on 2017-12-20

@author: liuqun
'''
import json

from alipay.aop.api.AlipayResponse import AlipayResponse
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.constant.ParamConstants import *
from alipay.aop.api.util.WebUtils import FileItem
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',
)
logger = logging.getLogger('')

configs = {
    P_SERVER_URL: "http://openapi-d5729.alipay.net/gateway.do",
    P_APP_ID: "2016123001274681",
    P_SIGN_TYPE: "RSA",
    P_APP_PRIVATE_KEY: "MIICXQIBAAKBgQC0saHSuyIaJz1EObe5CvvRX90FT95tpjIgJx+oG/qNfTqWCv7UC3yTF6ecBeaIxyRsxR3mrzqbQKTmYBkImZGMDqc9r4ORXurQpDqWh20tVdRfNKHhiDLb8CvGW5hXQ1C0KCxr73hcs475yNr9NMB7d+e6nKA8aRLjV3fT1zyvSQIDAQABAoGAGPaJYrGTroVJQ4mtxhSsYWqbAEbedcuGFUcSaoki/jUUyPHP7r9/gFq+PyHZjX/lmllJHjuLHzO5FFKmYrfEkZdu6MXdefv3lzE7vjVudZUdnmfh2yOB/OWOiWsJjzwThpcBJTtQusRJ4XdrdorS/gTBbcdeJbtxbITN1fjcWVkCQQDYzcWD6TCgQR8gHfCmZ2DcUrNZv1bVOzNMwqehUuPmkXJyb6XJ7CtuTMdpJKa9F4aKsF7Ne9JOsC9VRaKIUfkHAkEA1VyaIn3TGpFmnwDI6BKM3kzsj9YSb6Q8lb3cPMKWUfsuL3CJ2g4VpULwV/7HY4qfUVMb/6n0GHyanIKHEwWRLwJBAIKjKzsbDkPiOaEeqV17uW/JHW0c0HPYIkdEm8Gnss/CIJY4FEwh1OG3vgjrHtWeEWIMeHOVAtqLa1oUhaViz40CQQCasip7SZlvEO9D59DDGvgSEdoPK9pwIbdfpqnxT/CnfiPtd34roLym9xLF6k9s58w9rbGGPBZkTqvXQHhpHUc3AkAIODmnuHJi3UWw0UEnuz7Q+XS9iS46NSS6JmHYVeOLr0GoJhZmpGb1D9XnYtriEdh7gSha75Bz+yvbcLl4U9mP",
    P_ALIPAY_PUBLIC_KEY: "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDIgHnOn7LLILlKETd6BFRJ0GqgS2Y3mn1wMQmyh9zEyWlz5p1zrahRahbXAfCfSqshSNfqOmAQzSHRVjCqjsAw1jyqrXaPdKBmr90DIpIxmIyKXv4GGAkPyJ/6FTFY99uhpiq0qadD/uSzQsefWo0aTvP/65zi3eof7TcZ32oWpwIDAQAB",
    P_CHARSET: "gbk"
}


def simple_request():
    biz_params = {
        "key_a": "支付宝"
    }

    client = DefaultAlipayClient(configs, logger)
    response = None
    try:
        response = client.execute("alipay.open.app.fangzhong.test", {"biz_content": biz_params})
    except Exception as e:
        print(e)
    if not response:
        return

    alipay_response = AlipayResponse(response)
    if alipay_response.get_code() == '10000':
        response_object = json.loads(alipay_response.get_response_str())
        # 获取responseObject的各个属性
        # ...
    else:
        print(alipay_response.get_code() + '|' + alipay_response.get_msg() + '|' + alipay_response.get_sub_code() + \
              '|' + alipay_response.get_sub_msg())


def multipart_request():
    multipart_params = {
        'file_content': FileItem('IMG_2916.jpg', open("/Users/liuqun.lq/Downloads/IMG.jpg", 'rb').read()),
        'file_content2': FileItem('soapui-settings.txt', open("/Users/liuqun.lq/Downloads/soapui-settings.txt", 'rb').read()),
    }

    params = {
        "other_param": "支付宝"
    }

    client = DefaultAlipayClient(configs, logger)
    response = None

    response = client.multipart_execute("alipay.open.app.fangzhong.upload", params, multipart_params)

    alipay_response = AlipayResponse(response)
    if alipay_response.get_code() == '10000':
        response_object = json.loads(alipay_response.get_response_str())
        # 获取responseObject的各个属性
        # ...
    else:
        print(alipay_response.get_code() + '|' + alipay_response.get_msg() + '|' + alipay_response.get_sub_code() + \
              '|' + alipay_response.get_sub_msg())


def page_request():
    biz_params = {
        "key_a": "支付宝"
    }

    client = DefaultAlipayClient(configs, logger)

    response = client.page_execute("alipay.open.app.fangzhong.test", {"biz_content": biz_params}, "POST")
    print(response)

    response = client.page_execute("alipay.open.app.fangzhong.test", {"biz_content": biz_params}, "GET")
    print(response)


if __name__ == '__main__':
    simple_request()
    multipart_request()
    page_request()
