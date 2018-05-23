#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.constant.ParamConstants import *


class GoodsVO(object):

    def __init__(self):
        self._addition_desc = None
        self._barcode = None
        self._biz_status = None
        self._box_num = None
        self._cainiao_item_code = None
        self._category = None
        self._category_id = None
        self._goods_code = None
        self._goods_name = None
        self._last_operate_time = None
        self._last_operator = None
        self._origin_price = None
        self._price = None
        self._sale_limit = None
        self._specifications = None
        self._storage_time = None
        self._supplier_id = None

    @property
    def addition_desc(self):
        return self._addition_desc

    @addition_desc.setter
    def addition_desc(self, value):
        self._addition_desc = value
    @property
    def barcode(self):
        return self._barcode

    @barcode.setter
    def barcode(self, value):
        self._barcode = value
    @property
    def biz_status(self):
        return self._biz_status

    @biz_status.setter
    def biz_status(self, value):
        self._biz_status = value
    @property
    def box_num(self):
        return self._box_num

    @box_num.setter
    def box_num(self, value):
        self._box_num = value
    @property
    def cainiao_item_code(self):
        return self._cainiao_item_code

    @cainiao_item_code.setter
    def cainiao_item_code(self, value):
        self._cainiao_item_code = value
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value
    @property
    def category_id(self):
        return self._category_id

    @category_id.setter
    def category_id(self, value):
        self._category_id = value
    @property
    def goods_code(self):
        return self._goods_code

    @goods_code.setter
    def goods_code(self, value):
        self._goods_code = value
    @property
    def goods_name(self):
        return self._goods_name

    @goods_name.setter
    def goods_name(self, value):
        self._goods_name = value
    @property
    def last_operate_time(self):
        return self._last_operate_time

    @last_operate_time.setter
    def last_operate_time(self, value):
        self._last_operate_time = value
    @property
    def last_operator(self):
        return self._last_operator

    @last_operator.setter
    def last_operator(self, value):
        self._last_operator = value
    @property
    def origin_price(self):
        return self._origin_price

    @origin_price.setter
    def origin_price(self, value):
        self._origin_price = value
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value
    @property
    def sale_limit(self):
        return self._sale_limit

    @sale_limit.setter
    def sale_limit(self, value):
        self._sale_limit = value
    @property
    def specifications(self):
        return self._specifications

    @specifications.setter
    def specifications(self, value):
        self._specifications = value
    @property
    def storage_time(self):
        return self._storage_time

    @storage_time.setter
    def storage_time(self, value):
        self._storage_time = value
    @property
    def supplier_id(self):
        return self._supplier_id

    @supplier_id.setter
    def supplier_id(self, value):
        self._supplier_id = value


    def to_alipay_dict(self):
        params = dict()
        if self.addition_desc:
            if hasattr(self.addition_desc, 'to_alipay_dict'):
                params['addition_desc'] = self.addition_desc.to_alipay_dict()
            else:
                params['addition_desc'] = self.addition_desc
        if self.barcode:
            if hasattr(self.barcode, 'to_alipay_dict'):
                params['barcode'] = self.barcode.to_alipay_dict()
            else:
                params['barcode'] = self.barcode
        if self.biz_status:
            if hasattr(self.biz_status, 'to_alipay_dict'):
                params['biz_status'] = self.biz_status.to_alipay_dict()
            else:
                params['biz_status'] = self.biz_status
        if self.box_num:
            if hasattr(self.box_num, 'to_alipay_dict'):
                params['box_num'] = self.box_num.to_alipay_dict()
            else:
                params['box_num'] = self.box_num
        if self.cainiao_item_code:
            if hasattr(self.cainiao_item_code, 'to_alipay_dict'):
                params['cainiao_item_code'] = self.cainiao_item_code.to_alipay_dict()
            else:
                params['cainiao_item_code'] = self.cainiao_item_code
        if self.category:
            if hasattr(self.category, 'to_alipay_dict'):
                params['category'] = self.category.to_alipay_dict()
            else:
                params['category'] = self.category
        if self.category_id:
            if hasattr(self.category_id, 'to_alipay_dict'):
                params['category_id'] = self.category_id.to_alipay_dict()
            else:
                params['category_id'] = self.category_id
        if self.goods_code:
            if hasattr(self.goods_code, 'to_alipay_dict'):
                params['goods_code'] = self.goods_code.to_alipay_dict()
            else:
                params['goods_code'] = self.goods_code
        if self.goods_name:
            if hasattr(self.goods_name, 'to_alipay_dict'):
                params['goods_name'] = self.goods_name.to_alipay_dict()
            else:
                params['goods_name'] = self.goods_name
        if self.last_operate_time:
            if hasattr(self.last_operate_time, 'to_alipay_dict'):
                params['last_operate_time'] = self.last_operate_time.to_alipay_dict()
            else:
                params['last_operate_time'] = self.last_operate_time
        if self.last_operator:
            if hasattr(self.last_operator, 'to_alipay_dict'):
                params['last_operator'] = self.last_operator.to_alipay_dict()
            else:
                params['last_operator'] = self.last_operator
        if self.origin_price:
            if hasattr(self.origin_price, 'to_alipay_dict'):
                params['origin_price'] = self.origin_price.to_alipay_dict()
            else:
                params['origin_price'] = self.origin_price
        if self.price:
            if hasattr(self.price, 'to_alipay_dict'):
                params['price'] = self.price.to_alipay_dict()
            else:
                params['price'] = self.price
        if self.sale_limit:
            if hasattr(self.sale_limit, 'to_alipay_dict'):
                params['sale_limit'] = self.sale_limit.to_alipay_dict()
            else:
                params['sale_limit'] = self.sale_limit
        if self.specifications:
            if hasattr(self.specifications, 'to_alipay_dict'):
                params['specifications'] = self.specifications.to_alipay_dict()
            else:
                params['specifications'] = self.specifications
        if self.storage_time:
            if hasattr(self.storage_time, 'to_alipay_dict'):
                params['storage_time'] = self.storage_time.to_alipay_dict()
            else:
                params['storage_time'] = self.storage_time
        if self.supplier_id:
            if hasattr(self.supplier_id, 'to_alipay_dict'):
                params['supplier_id'] = self.supplier_id.to_alipay_dict()
            else:
                params['supplier_id'] = self.supplier_id
        return params

    @staticmethod
    def from_alipay_dict(d):
        if not d:
            return None
        o = GoodsVO()
        if 'addition_desc' in d:
            o.addition_desc = d['addition_desc']
        if 'barcode' in d:
            o.barcode = d['barcode']
        if 'biz_status' in d:
            o.biz_status = d['biz_status']
        if 'box_num' in d:
            o.box_num = d['box_num']
        if 'cainiao_item_code' in d:
            o.cainiao_item_code = d['cainiao_item_code']
        if 'category' in d:
            o.category = d['category']
        if 'category_id' in d:
            o.category_id = d['category_id']
        if 'goods_code' in d:
            o.goods_code = d['goods_code']
        if 'goods_name' in d:
            o.goods_name = d['goods_name']
        if 'last_operate_time' in d:
            o.last_operate_time = d['last_operate_time']
        if 'last_operator' in d:
            o.last_operator = d['last_operator']
        if 'origin_price' in d:
            o.origin_price = d['origin_price']
        if 'price' in d:
            o.price = d['price']
        if 'sale_limit' in d:
            o.sale_limit = d['sale_limit']
        if 'specifications' in d:
            o.specifications = d['specifications']
        if 'storage_time' in d:
            o.storage_time = d['storage_time']
        if 'supplier_id' in d:
            o.supplier_id = d['supplier_id']
        return o


