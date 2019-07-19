#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : exfilename.py
# @Author: Hu Zhu
# @Date  : 7/13
"""
从绝对路径中提取文件名带后缀
"""
import re
import os

class ExFileName:
    def __init__(self, ab_path):
        self.__path = ab_path
        self.__output = []

        (self._path, self.__filename) = os.path.split(self.__path)
        (self.__frontname, self.__extension) = os.path.splitext(self.__filename)

    def ex_filename(self):
        """
        在绝对路径中，提取带后缀的文件名
        :return: 返回带后缀的文件名
        """
        self.__output = self.__filename
        # self.__output = re.findall(r'[^\\/:*?"<>|\r\n]+$', self.__path)
        # print(type(self.__output), self.__path)
        # print(self.__output)
        return self.__output

    def extension_filenm(self):
        '''
        返回后缀名
        :return:
        '''
        # self.__output = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$',self.__path)
        self.__output = self.__extension
        # print(self.__output)
        return self.__output

    def ex_front_filenm(self):
        '''
        返回不带后缀的文件名
        :return:
        '''
        # self.__output = re.findall(r'[^\\/:*?"<>|\r\n]+$',self.__path)
        self.__output = self.__frontname
        # print(self.__output)
        return self.__output

# print(ExFileName('F:/Internship/11/guomi1_0Encrypted.rar').ex_front_filenm())