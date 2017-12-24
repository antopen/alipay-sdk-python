# -*- coding: utf-8 -*-
'''
Created on 2017-12-20

@author: liuqun
'''


def hasValuableKey(map, key):
    if not map:
        return False
    if not (key in map):
        return False
    if not map[key]:
        return False
    return True