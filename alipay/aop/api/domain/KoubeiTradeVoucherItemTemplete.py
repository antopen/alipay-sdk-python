#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.constant.ParamConstants import *
from alipay.aop.api.domain.KoubeiItemDescription import KoubeiItemDescription


class KoubeiTradeVoucherItemTemplete(object):

    def __init__(self):
        self._buyer_notes = None
        self._support_book = None
        self._validity_period = None
        self._validity_period_range_from = None
        self._validity_period_range_to = None
        self._validity_period_type = None
        self._verify_enable_times = None
        self._verify_frequency = None

    @property
    def buyer_notes(self):
        return self._buyer_notes

    @buyer_notes.setter
    def buyer_notes(self, value):
        if isinstance(value, list):
            self._buyer_notes = list()
            for i in value:
                if isinstance(i, KoubeiItemDescription):
                    self._buyer_notes.append(i)
                else:
                    self._buyer_notes.append(KoubeiItemDescription.from_alipay_dict(i))
    @property
    def support_book(self):
        return self._support_book

    @support_book.setter
    def support_book(self, value):
        self._support_book = value
    @property
    def validity_period(self):
        return self._validity_period

    @validity_period.setter
    def validity_period(self, value):
        self._validity_period = value
    @property
    def validity_period_range_from(self):
        return self._validity_period_range_from

    @validity_period_range_from.setter
    def validity_period_range_from(self, value):
        self._validity_period_range_from = value
    @property
    def validity_period_range_to(self):
        return self._validity_period_range_to

    @validity_period_range_to.setter
    def validity_period_range_to(self, value):
        self._validity_period_range_to = value
    @property
    def validity_period_type(self):
        return self._validity_period_type

    @validity_period_type.setter
    def validity_period_type(self, value):
        self._validity_period_type = value
    @property
    def verify_enable_times(self):
        return self._verify_enable_times

    @verify_enable_times.setter
    def verify_enable_times(self, value):
        self._verify_enable_times = value
    @property
    def verify_frequency(self):
        return self._verify_frequency

    @verify_frequency.setter
    def verify_frequency(self, value):
        self._verify_frequency = value


    def to_alipay_dict(self):
        params = dict()
        if self.buyer_notes:
            if isinstance(self.buyer_notes, list):
                for i in range(0, len(self.buyer_notes)):
                    element = self.buyer_notes[i]
                    if hasattr(element, 'to_alipay_dict'):
                        self.buyer_notes[i] = element.to_alipay_dict()
            if hasattr(self.buyer_notes, 'to_alipay_dict'):
                params['buyer_notes'] = self.buyer_notes.to_alipay_dict()
            else:
                params['buyer_notes'] = self.buyer_notes
        if self.support_book:
            if hasattr(self.support_book, 'to_alipay_dict'):
                params['support_book'] = self.support_book.to_alipay_dict()
            else:
                params['support_book'] = self.support_book
        if self.validity_period:
            if hasattr(self.validity_period, 'to_alipay_dict'):
                params['validity_period'] = self.validity_period.to_alipay_dict()
            else:
                params['validity_period'] = self.validity_period
        if self.validity_period_range_from:
            if hasattr(self.validity_period_range_from, 'to_alipay_dict'):
                params['validity_period_range_from'] = self.validity_period_range_from.to_alipay_dict()
            else:
                params['validity_period_range_from'] = self.validity_period_range_from
        if self.validity_period_range_to:
            if hasattr(self.validity_period_range_to, 'to_alipay_dict'):
                params['validity_period_range_to'] = self.validity_period_range_to.to_alipay_dict()
            else:
                params['validity_period_range_to'] = self.validity_period_range_to
        if self.validity_period_type:
            if hasattr(self.validity_period_type, 'to_alipay_dict'):
                params['validity_period_type'] = self.validity_period_type.to_alipay_dict()
            else:
                params['validity_period_type'] = self.validity_period_type
        if self.verify_enable_times:
            if hasattr(self.verify_enable_times, 'to_alipay_dict'):
                params['verify_enable_times'] = self.verify_enable_times.to_alipay_dict()
            else:
                params['verify_enable_times'] = self.verify_enable_times
        if self.verify_frequency:
            if hasattr(self.verify_frequency, 'to_alipay_dict'):
                params['verify_frequency'] = self.verify_frequency.to_alipay_dict()
            else:
                params['verify_frequency'] = self.verify_frequency
        return params

    @staticmethod
    def from_alipay_dict(d):
        if not d:
            return None
        o = KoubeiTradeVoucherItemTemplete()
        if 'buyer_notes' in d:
            o.buyer_notes = d['buyer_notes']
        if 'support_book' in d:
            o.support_book = d['support_book']
        if 'validity_period' in d:
            o.validity_period = d['validity_period']
        if 'validity_period_range_from' in d:
            o.validity_period_range_from = d['validity_period_range_from']
        if 'validity_period_range_to' in d:
            o.validity_period_range_to = d['validity_period_range_to']
        if 'validity_period_type' in d:
            o.validity_period_type = d['validity_period_type']
        if 'verify_enable_times' in d:
            o.verify_enable_times = d['verify_enable_times']
        if 'verify_frequency' in d:
            o.verify_frequency = d['verify_frequency']
        return o


