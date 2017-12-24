# -*- coding: utf-8 -*-
'''
Created on 2017-12-20

@author: liuqun
'''
import base64
import json
import rsa

from alipay.aop.api.util.StringUtils import *


def getSignContent(allParams, charset):
    signContent = ""
    for (k, v) in sorted(allParams.items()):
        value = v
        if not isinstance(value, str):
            value = json.dumps(value, ensure_ascii=False)
        signContent += ("&" + k + "=" + value)
    signContent = signContent[1:]
    return signContent.encode(charset)

def fillPrivateKeyMarker(privateKey):
    return addStartEnd(privateKey, "-----BEGIN RSA PRIVATE KEY-----\n", "\n-----END RSA PRIVATE KEY-----")


def fillPublicKeyMarker(publicKey):
    return addStartEnd(publicKey, "-----BEGIN PUBLIC KEY-----\n", "\n-----END PUBLIC KEY-----")


def signWithRSA(privateKey, signContent):
    privateKey = fillPrivateKeyMarker(privateKey)
    signature = rsa.sign(signContent, priv_key=rsa.PrivateKey.load_pkcs1(privateKey, format='PEM'), hash='SHA-1')
    return base64.b64encode(signature)


def signWithRSA2(privateKey, signContent):
    privateKey = fillPrivateKeyMarker(privateKey)
    signature = rsa.sign(signContent, priv_key=rsa.PrivateKey.load_pkcs1(privateKey, format='PEM'), hash='SHA-256')
    return base64.b64encode(signature)


def verifyWithRSA(publicKey, message, sign):
    publicKey = fillPublicKeyMarker(publicKey)
    sign = base64.b64decode(sign)
    return rsa.verify(message, sign, rsa.PublicKey.load_pkcs1_openssl_pem(publicKey))

