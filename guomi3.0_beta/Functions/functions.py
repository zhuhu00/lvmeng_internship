#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : functions.py
# @Author: Hu Zhu
# @Date  : 7/13
"""
存储了许多函数，有关设备操作的
其中需要对函数进行修改，统一为类或者函数

"""

import ctypes
import sys
from Functions.loaddll import LoadDll
from Functions.paras import Bool, szName, Ulong, PulEn
from FileOperate.fileoperate import FileReader, FileWriter


def SKF_EnumDev(bool):
    '''
    Enum the dev
    :param bool:int
    :param sznamelist:int or other types
    :param pulsize: int
    :return: the code number
    for instance:
    SKF_EnumDev(1,1)
    '''

    pulsize = ctypes.c_ulong()  # pulsize主要为输出值，为输出值得时候，返回namelist的大小，一开始可以为空
    enum_result1 = LoadDll().get().SKF_EnumDev(Bool(bool).get(), ctypes.c_byte(), ctypes.byref(pulsize))
    if enum_result1 == 0:
        print('第一次设备枚举成功，返回 : ' + str(enum_result1))  # + "\n设备名称所占空间大小为：" + str(pulsize.value))
    else:
        print("第一次设备枚举失败，返回错误码：" + str(enum_result1))
        sys.exit(1)
    namelist = ctypes.c_byte(pulsize.value)
    enum_result2 = LoadDll().get().SKF_EnumDev(Bool(bool).get(), ctypes.byref(namelist), ctypes.byref(pulsize))
    if enum_result2 == 0:
        print('第二次设备枚举成功，返回 : ' + str(enum_result2) + '\n设备名字为：' + str(chr(namelist.value)))
    else:
        print("第二次设备枚举失败，返回错误码：" + str(enum_result2))
        sys.exit(1)
    return namelist.value  # 返回的值是namelist


def SKF_ConnectDev(LPSTR):
    '''
    LPSTR表示设备列表
    instance：
    SKF_ConnectDev(namelist)
    :return:
    :param LPSTR: szName
    :param DEVHANDLE: *Dev
    '''
    size = 16
    handle = ctypes.create_string_buffer(size)  # 创建一个16的char数组，用于返回句柄
    c_result = LoadDll().get().SKF_ConnectDev(ctypes.byref(szName(LPSTR).get()), ctypes.byref(handle))
    if c_result == 0:
        print('设备连接成功，返回 : ' + str(c_result))
    else:
        print("设备连接失败，返回错误码：" + str(c_result))
        sys.exit(1)
    return handle


# 明文导入密钥
class SKF_SetSymmKey(LoadDll):
    '''
    instance:
    Test = SKF_SetSymmKey(hDev(1), pbKey(1), ulAlgID(1), phKey('1'))
    print(Test.get())
    '''

    def __init__(self, hdev):
        LoadDll.__init__(self)
        size = 16
        # hdev = ctypes.c_void_p(size)
        pbkey = ctypes.create_string_buffer(size)
        i = 0
        while i < size:
            pbkey[i] = 1
            i += 1
        ulalgID = ctypes.c_ulong(0x00000101)  # 设置加密方式
        phkey = ctypes.c_byte(10)
        _hdev = int.from_bytes(hdev[0], byteorder='big', signed=False)
        # hdev = ctypes.c_int(1)
        self.__output = LoadDll.get(self).SKF_SetSymmKey(_hdev, ctypes.byref(pbkey), ulalgID, ctypes.byref(phkey))
        if self.__output == 0:
            print('明文导入密钥成功，返回 : ' + str(self.__output))
        else:
            print("明文导入密钥失败，返回错误码： " + str(self.__output))
            # sys.exit(1)
        self.__phkey = phkey

    def getphkey(self):
        return self.__phkey


# 加密初始化
def SKF_EncryptInit(hkey):
    '''
    hkey 需要输入，另外需要再函数内部进行修改结构体的值
    :param hkey:
    :return:
    instance
    result = SKF_EncryptInit(1)
    '''
    parm = StructPara()
    parm.PadddingType = ctypes.c_ulong(0)
    parm.FeedBitLen = ctypes.c_ulong(0)
    parm.IVLen = ctypes.c_ulong(0)
    eninit_result = LoadDll().get().SKF_EncryptInit(hkey, parm)
    if eninit_result == 0:
        print('加密初始化连接成功，返回 : ' + str(eninit_result))
    else:
        print("加密初始化连接失败，错误码返回：" + str(eninit_result))
        sys.exit(1)


# 多组数据加密
def SKF_EncryptUpdate(hkey, pbdata, lenpbdata):
    '''
    多组数据加密：
    :param hkey: 密钥句柄
    :param pbdata: 待加密数据
    :param lenpbdata: 待加密数据长度
    :return:返回加密后的数据和加密后的数据长度
    enerypteddata: 加密后的数据
     pulencry.value：加密后数据长度
    '''

    lenpbdataa = Ulong(lenpbdata).get()  # 加密数据的长度
    enerypteddata = ctypes.create_string_buffer(lenpbdata)  # 加密后的数据
    pulencry = PulEn(lenpbdata).get()  # 返回加密后的数据长度
    en_result = LoadDll().get().SKF_EncryptUpdate(hkey, ctypes.byref(pbdata), lenpbdataa,
                                                  ctypes.byref(enerypteddata), ctypes.byref(pulencry))
    if en_result == 0:
        print('加密成功，返回 : ' + str(en_result))
    else:
        print("加密失败，返回错误码 : " + str(en_result))
        sys.exit(1)

    return enerypteddata, pulencry.value


def SKF_EncryptFinal(handle, encryteddata):
    '''
    encrypt final
    :param handle: int type
    :param byte: int type
    :param ulong: int type
    :return: code number
    instance:  hh = SKF_EncryptFinal(1,2,3)

    '''
    lendata = ctypes.c_ulong(len(encryteddata))
    enf_result = LoadDll().get().SKF_EncryptFinal(handle, ctypes.byref(encryteddata), ctypes.byref(lendata))
    if enf_result == 0:
        print('加密结束成功，返回 : ' + str(enf_result))
    else:
        print("加密结束失败，错误码为 : " + str(enf_result))
        sys.exit(1)
    lendata = len(encryteddata)  # 长度
    return encryteddata, lendata  # 数据以及长度


class SKF_DisconnectDev(LoadDll):
    '''
    instance
    SKF_DisconnectDev(hDev(int))
    :return coded number
    test = SKF_DisconnectDev(hDev(1))
    print(test.get())
    '''

    def __init__(self, hdev):
        LoadDll.__init__(self)
        self.__output = LoadDll.get(self).SKF_DisconnectDev(hdev)

    def get(self):
        return self.__output


class StructPara(ctypes.Structure):
    _fields_ = [("IV", ctypes.c_char * 32),
                ("IVLen", ctypes.c_ulong),
                ("PadddingType", ctypes.c_ulong),
                ("FeedBitLen", ctypes.c_ulong)]


# 解秘初始化
def SKF_DecryptInit(hkey):
    parm = StructPara()
    parm.PadddingType = ctypes.c_ulong(0)
    parm.FeedBitLen = ctypes.c_ulong(0)
    parm.IVLen = ctypes.c_ulong(0)
    eninit_result = LoadDll().get().SKF_DecryptInit(hkey, parm)
    if eninit_result == 0:
        print('解密初始化连接成功，返回 : ' + str(eninit_result))
    else:
        print("解密初始化连接失败，返回" + str(eninit_result))
        sys.exit(1)


# 多组数据解密
def SKF_DecryptUpdate(hkey, endata, lenendata):
    lenendataa = Ulong(lenendata).get()  # 解密数据的长度
    decrypteddata = ctypes.create_string_buffer(lenendata)  # 解密后的数据
    pulencry = PulEn(lenendata).get()  # 返回解密后的数据长度
    de_result = LoadDll().get().SKF_DecryptUpdate(hkey, ctypes.byref(endata), lenendataa,
                                                  ctypes.byref(decrypteddata), ctypes.byref(pulencry))
    if de_result == 0:
        print('解密成功，返回 : ' + str(de_result))
    else:
        print("解密失败，返回 : " + str(de_result))
        sys.exit(1)
    # for ii in range(pulencry.value):
    #     print(decrypteddata[ii])
    return decrypteddata, len(decrypteddata)


def SKF_DecryptFinal(hkey, decryteddata):
    # print(handle)
    # print(encryteddata, lengthdata)
    lengthdata = ctypes.c_ulong(len(decryteddata))
    # lengthdata = ctypes.create_string_buffer(32)
    lendata = ctypes.c_ulong()
    definal_result = LoadDll().get().SKF_EncryptFinal(hkey, ctypes.byref(decryteddata), ctypes.byref(lendata))
    if definal_result == 0:
        print('解密结束成功，返回 : ' + str(definal_result))
    else:
        print("解密结束失败，返回 : " + str(definal_result))
        sys.exit(1)
    return decryteddata, lengthdata


def bigfileencrypt(epath, dpath, isEn):
    '''
    先进行文件读取，按照每一块处理数据，应该加密前的东西可以只执行一次，
    之后的是加密重复执行，针对每一次的block，进行加密和保存文件
    :param epath:
    :param dpath:
    :param isEn:
    :return:
    '''
    fileInfo = FileReader(epath)

    szname = SKF_EnumDev(1)  # 枚举设备
    phdev = SKF_ConnectDev(szname)  # 连接设备
    hkey = SKF_SetSymmKey(phdev).getphkey()  # 明文导入密钥
    SKF_EncryptInit(hkey)  # 加密初始化

    for block in fileInfo.read():
        lenfileInfo = len(block)

        dataNeedEn = ctypes.create_string_buffer(lenfileInfo)
        for i in range(lenfileInfo):
            dataNeedEn[i] = int(block[i])
        lenDataNeedEn = len(dataNeedEn)
        [eneddata, leneneddata] = SKF_EncryptUpdate(hkey, dataNeedEn, lenDataNeedEn)
        SKF_EncryptFinal(hkey, eneddata)
        enpath = FileWriter(epath, dpath, eneddata, isEn).write()
    print(epath + '文件加密完成\n' + '加密文件保存路径为：' + str(enpath))


def bigfiledecrypt(epath, dpath, isEn):
    fileInfo = FileReader(epath)
    szname = SKF_EnumDev(1)  # 枚举设备
    phdev = SKF_ConnectDev(szname)  # 连接设备
    hkey = SKF_SetSymmKey(phdev).getphkey()  # 明文导入密钥
    SKF_DecryptInit(hkey)  # 解密初始化

    for block in fileInfo.read():
        lenenfile = len(block)
        eneddataa = ctypes.create_string_buffer(lenenfile)
        for i in range(lenenfile):
            eneddataa[i] = int(block[i])

        [deeddata, lendeeddata] = SKF_DecryptUpdate(hkey, eneddataa, lenenfile)

        # 解密结束
        SKF_DecryptFinal(hkey, deeddata)
        outpath = FileWriter(epath, dpath, deeddata, isEn).write()
    print(epath + '文件解密完成\n' + '解密后文件保存路径为：' + str(outpath))
