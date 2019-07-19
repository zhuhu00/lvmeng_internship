#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : fun_sum.py
# @Author: Hu Zhu
# @Date  : 7/7
import ctypes
from FileOperate.fileoperate import FileReader, FileWriter
from Functions.functions import SKF_EnumDev, SKF_ConnectDev, SKF_SetSymmKey, SKF_EncryptInit, SKF_EncryptUpdate, SKF_EncryptFinal, \
    SKF_DecryptInit, SKF_DecryptUpdate, SKF_DecryptFinal


class EnOrDe:
    def __init__(self, epath, dpath, isEn):
        self.__epath = epath
        self.__dpath = dpath
        self.__isEn = isEn

    def bigfileencrypt(self):
        """
        先进行文件读取，按照每一块处理数据，应该加密前的东西可以只执行一次，
        之后的是加密重复执行，针对每一次的block，进行加密和保存文件
        :param epath:
        :param dpath:
        :param isEn:
        :return:
        """
        fileInfo = FileReader(self.__epath)

        szname = SKF_EnumDev(1)  # 枚举设备
        phdev = SKF_ConnectDev(szname)  # 连接设备
        hkey = SKF_SetSymmKey(phdev).getphkey()  # 明文导入密钥
        SKF_EncryptInit(hkey)  # 加密初始化
        # inpath = ''
        # print('jiami')
        # print(len(fileInfo.read()))
        # 第一次写入的时候，重写该文件，之后都是添加写入，
        flag = 1

        for block in fileInfo.read():

            lenfileInfo = len(block)
            dataNeedEn = ctypes.create_string_buffer(lenfileInfo)
            for i in range(lenfileInfo):
                dataNeedEn[i] = int(block[i])
            lenDataNeedEn = len(dataNeedEn)
            [eneddata, leneneddata] = SKF_EncryptUpdate(hkey, dataNeedEn, lenDataNeedEn)
            SKF_EncryptFinal(hkey, eneddata)

            inpath = FileWriter(self.__epath, self.__dpath, eneddata, self.__isEn, flag).write()
            flag += 1
            # print(flag)
        print(self.__epath + '文件加密完成\n' + '加密文件保存路径为：' + str(inpath))

    def bigfiledecrypt(self):
        fileInfo = FileReader(self.__epath)
        szname = SKF_EnumDev(1)  # 枚举设备
        phdev = SKF_ConnectDev(szname)  # 连接设备
        hkey = SKF_SetSymmKey(phdev).getphkey()  # 明文导入密钥
        SKF_DecryptInit(hkey)  # 解密初始化

        # 第一次写入的时候，重写该文件，之后都是添加写入，
        flag = 1

        for block in fileInfo.read():
            lenenfile = len(block)
            eneddataa = ctypes.create_string_buffer(lenenfile)
            for i in range(lenenfile):
                eneddataa[i] = int(block[i])

            [deeddata, lendeeddata] = SKF_DecryptUpdate(hkey, eneddataa, lenenfile)

            # 解密结束
            SKF_DecryptFinal(hkey, deeddata)
            flag += 1
            outpath = FileWriter(self.__epath, self.__dpath, deeddata, self.__isEn, flag).write()
            # print(outpath)
        print(outpath)
        # print(self.__epath + '文件解密完成\n' + '解密后文件保存路径为：' + str(outpath))


def entry(epath, dpath, isEn):
    if 1 == isEn:
        # for i in len()
        EnOrDe(epath, dpath, isEn).bigfileencrypt()
    elif 0 == isEn:
        EnOrDe(epath, dpath, isEn).bigfiledecrypt()

# enpath = ['F:/Internship/20190710/xswlEncrypted.txt','F:/Internship/20190710/Encryptedfile.txt']
# # # depath = 'F:/Internship/20190710/Encryptedfile.txt'
# # enpath = 'F:/Internship/20190710/Encryptedfile.txt'
# depath = 'F:/Internship/20190710'
# for i in range(len(enpath)):
#     entry(enpath[i], depath, 0)
