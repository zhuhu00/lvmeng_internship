#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : paras.py
# @Author: Hu Zhu
# @Date  : 7/10
import ctypes


class Bool:
    def __init__(self, para):
        self.__para = para

    def get(self):
        if isinstance(self.__para, int):
            return ctypes.c_byte(self.__para)
        else:
            print("Bool types error")


# class szNameList:
#     '''
#     para for OUT, privide the buffer
#     '''
#
#     def __init__(self, para=0):
#         self.__para = para
#
#     def get(self):
#         return ctypes.create_string_buffer(self.__para)
# LPSTR char* in
class szName:
    def __init__(self, para):
        self.__para = para

    def get(self):
        if isinstance(self.__para, int):
            return ctypes.c_char_p(self.__para)
            # return ctypes.create_string_buffer(self.__para)
        else:
            print('type error')


class Ulong:
    def __init__(self, para):
        self.__para = para

    def get(self):
        if isinstance(self.__para, int):  # check
            return ctypes.c_int(self.__para)
        else:
            print("Ulong type error")


class PulEn:
    def __init__(self, para):
        self.__para = para

    def get(self):
        if isinstance(self.__para, int):  # check
            return ctypes.c_int(self.__para)
        else:
            print("PulEn type error")
