# -*- coding: utf-8 -*-
'''
Created on 2017-12-20

@author: liuqun
'''
import json

from alipay.aop.api.constant.CommonConstants import *

try:
    import httplib
except ImportError:
    import http.client as httplib
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse
try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus
import mimetypes

from alipay.aop.api.exception.Exception import *
from alipay.aop.api.constant.ParamConstants import *
from alipay.aop.api.util.CommonUtils import *


class FileItem(object):
    def __init__(self, filename=None, content=None):
        self.filename = filename
        self.content = content


class MultiPartForm(object):
    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = "ALIPAY_PYTHON_SDK_BOUNDARY"
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        self.form_fields.append((name, str(value)))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, body))
        return


def urlencode(params, charset):
    queryString = ""
    for (k, v) in params.items():
        value = v
        if not isinstance(value, str):
            value = json.dumps(value, ensure_ascii=False)
        value = quote_plus(value)
        queryString += ("&" + k + "=" + value)
    queryString = queryString[1:]
    return queryString


def post(url, queryString=None, headers=None, params=None, timeout=15):
    urlParseResult = urlparse.urlparse(url)
    host = urlParseResult.hostname
    port = 80
    connection = httplib.HTTPConnection(host, port, False, timeout)
    if url.find("https") == 0:
        port = 443
        connection = httplib.HTTPSConnection(host, port, False, timeout)
    url = urlParseResult.scheme + "://" + urlParseResult.hostname
    if urlParseResult.port:
        url += urlParseResult.port
    url += urlParseResult.path
    url += ('?' + queryString)

    try:
        connection.connect()
    except Exception as e:
        raise RequestException('[' + THREAD_LOCAL.uuid + ']post connect failed. ' + str(e))
    body = None
    charset = 'utf-8'
    if hasValuableKey(params, P_CHARSET):
        charset = params["charset"]
    if params:
        body = urlencode(params, charset)
    try:
        connection.request("POST", url, body=body, headers=headers)
    except Exception as e:
        raise RequestException('[' + THREAD_LOCAL.uuid + ']post request failed. ' + str(e))
    response = connection.getresponse()
    if response.status is not 200:
        raise ResponseException('[' + THREAD_LOCAL.uuid + ']invalid http status ' + str(response.status) + \
                               ',detail body:' + response.read())
    result = response.read()
    try:
        response.close()
        connection.close()
    except Exception as e:
        pass
    return result




