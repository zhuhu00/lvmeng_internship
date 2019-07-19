#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : loaddll.py
# @Author: Hu Zhu
# @Date  : 7/13
import ctypes

class LoadDll:
    def __init__(self, path='..\\Thrift\\back\\SKF_3310S-T.dll'):
        self.path = path
        self.__dllInterface = ctypes.windll.LoadLibrary(self.path)

    def get(self):
        return self.__dllInterface
