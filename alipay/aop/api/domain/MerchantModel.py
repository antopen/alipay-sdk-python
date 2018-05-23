#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.constant.ParamConstants import *


class MerchantModel(object):

    def __init__(self):
        self._alias_name = None
        self._contact_name = None
        self._contact_number = None
        self._name = None

    @property
    def alias_name(self):
        return self._alias_name

    @alias_name.setter
    def alias_name(self, value):
        self._alias_name = value
    @property
    def contact_name(self):
        return self._contact_name

    @contact_name.setter
    def contact_name(self, value):
        self._contact_name = value
    @property
    def contact_number(self):
        return self._contact_number

    @contact_number.setter
    def contact_number(self, value):
        self._contact_number = value
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


    def to_alipay_dict(self):
        params = dict()
        if self.alias_name:
            if hasattr(self.alias_name, 'to_alipay_dict'):
                params['alias_name'] = self.alias_name.to_alipay_dict()
            else:
                params['alias_name'] = self.alias_name
        if self.contact_name:
            if hasattr(self.contact_name, 'to_alipay_dict'):
                params['contact_name'] = self.contact_name.to_alipay_dict()
            else:
                params['contact_name'] = self.contact_name
        if self.contact_number:
            if hasattr(self.contact_number, 'to_alipay_dict'):
                params['contact_number'] = self.contact_number.to_alipay_dict()
            else:
                params['contact_number'] = self.contact_number
        if self.name:
            if hasattr(self.name, 'to_alipay_dict'):
                params['name'] = self.name.to_alipay_dict()
            else:
                params['name'] = self.name
        return params

    @staticmethod
    def from_alipay_dict(d):
        if not d:
            return None
        o = MerchantModel()
        if 'alias_name' in d:
            o.alias_name = d['alias_name']
        if 'contact_name' in d:
            o.contact_name = d['contact_name']
        if 'contact_number' in d:
            o.contact_number = d['contact_number']
        if 'name' in d:
            o.name = d['name']
        return o


