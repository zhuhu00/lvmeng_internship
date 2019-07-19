#!/usr/bin/env python
# -*- coding:utf-8; -*-

import sys
import time
import os
from FileTransfer.FileClient import ipaddr

print("hello world")
sys.path.insert(0, os.getcwd() + "\\base")
from Thrift.interface import info
from Thrift.base.ThriftClient import ThriftClient
from Thrift.base.IpAddress import IpAddress
# ipaddr = input("请输入需要连接的ip地址：")
# ipaddr = '172.16.4.55'
# ipaddr = '169.254.21.210'
client = ThriftClient(IpAddress(ipaddr, 8080), info)
'''
sender = client.create()

print("start to ping")
##sender.ping()

sender.start("222222222222", True)
sender.ping()

def GetPath(self, PassAddress, enCodedP, SavePath):
    PathList = PassAddress.split('+',1)
    print(PassAddress)
    enCodedP = PathList[0]
    SavePath = PathList[1]
    print(enCodedP)
    print(SavePath)

GetPath()

print("finish to ping")


#界面

'''
