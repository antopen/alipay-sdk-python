#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.constant.ParamConstants import *
from alipay.aop.api.domain.AlipayUserPrincipalInfo import AlipayUserPrincipalInfo


class AlipayUserSceneCooperationConsultModel(object):

    def __init__(self):
        self._principal = None
        self._scene = None

    @property
    def principal(self):
        return self._principal

    @principal.setter
    def principal(self, value):
        if isinstance(value, AlipayUserPrincipalInfo):
            self._principal = value
        else:
            self._principal = AlipayUserPrincipalInfo.from_alipay_dict(value)
    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, value):
        self._scene = value


    def to_alipay_dict(self):
        params = dict()
        if self.principal:
            if hasattr(self.principal, 'to_alipay_dict'):
                params['principal'] = self.principal.to_alipay_dict()
            else:
                params['principal'] = self.principal
        if self.scene:
            if hasattr(self.scene, 'to_alipay_dict'):
                params['scene'] = self.scene.to_alipay_dict()
            else:
                params['scene'] = self.scene
        return params

    @staticmethod
    def from_alipay_dict(d):
        if not d:
            return None
        o = AlipayUserSceneCooperationConsultModel()
        if 'principal' in d:
            o.principal = d['principal']
        if 'scene' in d:
            o.scene = d['scene']
        return o


