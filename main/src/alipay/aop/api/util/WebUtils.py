# -*- coding: utf-8 -*-
'''
Created on 2017-12-20

@author: liuqun
'''
import json
import os

import itertools

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


class FileItem(object):
    def __init__(self, filename=None, content=None):
        self.filename = filename
        self.content = content


class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self, charset='utf-8'):
        self.charset = charset
        self.form_fields = []
        self.files = []
        self.boundary = "ALIPAY_SDK_PYTHON_BOUNDARY"
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        if not isinstance(value, str):
            value = json.dumps(value, ensure_ascii=False)
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, fileContent, mimetype=None):
        """Add a file to be uploaded."""
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, fileContent))
        return

    def build_body(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.
        parts = []
        part_boundary = '--' + self.boundary

        # Add the form fields
        parts.extend(
            [bytes(part_boundary.encode(self.charset)),
             bytes(('Content-Disposition: form-data; name="%s"' % name).encode(self.charset))
                if PYTHON_VERSION_3 else ('Content-Disposition: form-data; name="%s"' % name),
             bytes(('Content-Type: text/plain; charset=%s' % self.charset).encode(self.charset)),
             bytes(''.encode(self.charset)),
             bytes(value.encode(self.charset)) if PYTHON_VERSION_3 else value
            ]
            for name, value in self.form_fields
        )

        # Add the files to upload
        parts.extend(
            [bytes(part_boundary.encode(self.charset)),
             bytes(('Content-Disposition: form-data; name="%s"; filename="%s"' %
                    (field_name, filename)).encode(self.charset)) if PYTHON_VERSION_3 else
                    ('Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename)),
             bytes(('Content-Type: %s' % content_type).encode(self.charset)),
             bytes('Content-Transfer-Encoding: binary'.encode(self.charset)),
             bytes(''.encode(self.charset)),
             body,
            ]
            for field_name, filename, content_type, body in self.files
        )

        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append(bytes(('--' + self.boundary + '--').encode(self.charset)))
        flattened.append(bytes(''.encode(self.charset)))
        return bytes('\r\n'.encode(self.charset)).join(flattened)


def urlencode(params, charset):
    queryString = ""
    for (k, v) in params.items():
        value = v
        if not isinstance(value, str):
            value = json.dumps(value, ensure_ascii=False)
        if PYTHON_VERSION_3:
            value = quote_plus(value, encoding=charset)
        else:
            value = quote_plus(value)
        queryString += ("&" + k + "=" + value)
    queryString = queryString[1:]
    return queryString


def getHttpConnection(url, queryString, timeout):
    urlParseResult = urlparse.urlparse(url)
    host = urlParseResult.hostname
    port = 80
    connection = httplib.HTTPConnection(host=host, port=port, timeout=timeout)
    if url.find("https") == 0:
        port = 443
        connection = httplib.HTTPSConnection(host=host, port=port, timeout=timeout)
    url = urlParseResult.scheme + "://" + urlParseResult.hostname
    if urlParseResult.port:
        url += urlParseResult.port
    url += urlParseResult.path
    url += ('?' + queryString)
    return (url, connection)


def post(url, queryString=None, headers=None, params=None, charset='utf-8', timeout=15):
    url, connection = getHttpConnection(url, queryString, timeout)

    try:
        connection.connect()
    except Exception as e:
        raise RequestException('[' + THREAD_LOCAL.uuid + ']post connect failed. ' + str(e))
    body = None
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
    except Exception:
        pass
    return result


def multipartPost(url, queryString=None, headers=None, params=None, multipartParams=None, charset='utf-8', timeout=30):
    url, connection = getHttpConnection(url, queryString, timeout)

    try:
        connection.connect()
    except Exception as e:
        raise RequestException('[' + THREAD_LOCAL.uuid + ']post connect failed. ' + str(e))

    form = MultiPartForm(charset)
    for key, value in params.items():
        form.add_field(key, value)
    for key, value in multipartParams.items():
        fileItem = value
        if (fileItem and isinstance(fileItem, FileItem)):
            form.add_file(key, fileItem.filename, fileItem.content)
    body = form.build_body()
    if not headers:
        headers = {}
    headers['Content-type'] = form.get_content_type()

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
    except Exception:
        pass
    return result
