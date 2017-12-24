# -*- coding: utf-8 -*-
'''
Created on 2017-12-20

@author: liuqun
'''
import re
import threading


ALIPAY_SDK_PYTHON_VERSION = "alipay-sdk-python-1.0.0.20171220"

PATTERN_RESPONSE_BEGIN = re.compile(r'(\"[a-zA-z_]+_response\"[ \t\n]*:[ \t\n]*\{)')
PATTERN_RESPONSE_SIGN_BEGIN = re.compile(r'(\}[ \t\n]*,[ \t\n]*\"sign\"[ \t\n]*:[ \t\n]*\")')

THREAD_LOCAL = threading.local()