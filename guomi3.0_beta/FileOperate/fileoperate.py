#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : fileoperate.py
# @Author: Hu Zhu
# @Date  : 7/13
# 将大文件分块读取或者写入的函数以及类
import sys
from FileOperate.exfilename import ExFileName
import os

# 文件读取只有一个文件地址参数
class FileReader:
    def __init__(self, filepath):
        """
        文件按照2的20次方的大小分块读取
        :param filepath: 输入为文件地址
        """
        self.BLOCK_SIZE = 1048576
        self.filepath = filepath
        self.SIZE = 0

    def read(self):
        """
        文件读取操作，对文件进行二进制读取，这样方便读取和写入
        :return: 文件的二进制block
        """
        f = open(self.filepath, 'rb')
        while True:
            block = f.read(self.BLOCK_SIZE)
            if block:
                self.SIZE += block.__len__()
                yield (block)
            else:
                f.close()
                return


# 文件读取需要有四个参数，分别是输入文件，输出文件夹，写入内容，是否加密，最后返回处理后的文件路径
class FileWriter:
    def __init__(self, in_filepath, out_filepath, content, isEn, flag):
        self.__in_filepath = in_filepath
        self.__out_filepath = out_filepath
        self.content = content
        self.SIZE = 0
        self.__isEn = isEn
        self.__flag = flag
        self.__filename = ExFileName(in_filepath).ex_filename()
        self.__frontname = ExFileName(in_filepath).ex_front_filenm()
        self.__extensionnm = ExFileName(in_filepath).extension_filenm()
        self.filepath = ''

        # 加密为1，解密为0
        if 1 == self.__isEn:
            self.filepath = self.__out_filepath + "\\" + self.__frontname + 'Encrypted' + self.__extensionnm
        elif 0 == self.__isEn:
            self.filepath = self.__out_filepath + "\\" + self.__frontname + 'Decrypted' + self.__extensionnm
        else:
            print('非理想文件写入，请重新打开程序！！！')
            sys.exit(1)

    def write(self):
        e_path = os.path.dirname(self.filepath)
        if not os.path.exists(e_path):
            os.makedirs(e_path)

        if 1 == self.__flag:
            with open(self.filepath, 'wb') as f:
                f.write(self.content)
        else:
            with open(self.filepath, 'ab') as f:
                f.write(self.content)

        # with open(self.filepath, 'ab') as f:
        #     f.write(self.content)
        self.SIZE += self.content.__len__()
        return self.filepath
