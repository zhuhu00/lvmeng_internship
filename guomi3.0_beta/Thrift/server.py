#!/usr/bin/env python
# -*- coding:utf-8; -*-

import sys
import os
from base.ThriftServer import ThriftServer
from base.IpAddress import IpAddress
from handler import InfoHandler
from interface import info
import socket
import hashlib
import threading

print("server端开启")
sys.path.insert(0, os.getcwd() + "\\base")
# 导入THRIFT库
# print(sys.path)
# 获取ip地址
hostname = socket.gethostname()
ipaddr = socket.gethostbyname(hostname)
print('本机ip地址为：' + str(ipaddr))
# ipaddr = '192.168.1.185'

def thrift_server():
    handler = InfoHandler()

    server = ThriftServer(handler, IpAddress(ipaddr, 8080), info)
    # ThriftServer(handler, self.__ipAddress, wipsService)
    server.createServer()
    server.start()


def file_server():
    # 开启文件传输的服务
    f_server = socket.socket()
    f_server.bind((ipaddr, 8081))

    f_server.listen(5)

    print("监听开始（用于传输文件）。。。。")
    while True:
        conn, addr = f_server.accept()  # 等待连接

        print("文件传输部分的网络参数为" + "conn:", conn, "\naddr:", addr)  # conn连接实例

        while True:
            data = conn.recv(1024)  # 接收
            if not data:  # 客户端已断开
                print("客户端断开连接")
                break

            print("收到的命令：", data.decode("utf-8"))

            rec_command = data.decode("utf-8")
            cmd = rec_command[0:4]
            filename_string = rec_command[5:]

            if "cget" == cmd:
                # 为客户端接收
                filename_list = filenamee(filename_string)
                # c_get(filename_string)
                for i in range(len(filename_list)):
                    if 4 > len(filename_list[i]):
                        pass
                    else:
                        if os.path.isfile(filename_list[i]):  # 判断文件存在

                            # 1.先发送文件大小，让客户端准备接收
                            size = os.stat(filename_list[i]).st_size  # 获取文件大小
                            conn.send(str(size).encode("utf-8"))  # 发送数据长度
                            print("发送的大小：", size)

                            # 2.发送文件内容
                            conn.recv(1024)  # 接收确认

                            m = hashlib.md5()
                            f = open(filename_list[i], "rb")
                            for line in f:
                                conn.send(line)  # 发送数据
                                m.update(line)
                            f.close()

                            # 3.发送md5值进行校验
                            md5 = m.hexdigest()
                            conn.send(md5.encode("utf-8"))  # 发送md5值
                            print("md5:", md5)

            if "sget" == cmd:
                # 服务器接收文件
                client_responce = conn.recv(1024)  # 传文件大小
                file_size = int(client_responce.decode("utf-8"))
                print("传输的文件大小为：", file_size)

                # 2 准备接受文件
                conn.send("准备好接收".encode('utf-8'))
                filename_list = filenamee(filename_string)
                for i in range(len(filename_list)):
                    if 4 > len(filename_list[i]):
                        pass
                    else:
                        # 开始接收文件
                        # 如果文件目录不存在，则创建该目录
                        e_path = os.path.dirname(filename_list[i])
                        if not os.path.exists(e_path):
                            os.makedirs(e_path)
                        f = open(filename_list[i], 'wb')
                        print(filename_list[i])
                        received_size = 0
                        m = hashlib.md5()

                        while received_size < file_size:
                            # size = 0  # 准确接收数据大小，解决粘包
                            if file_size - received_size > 1024:  # 多次接收
                                size = 1024
                            else:  # 最后一次接收完毕
                                size = file_size - received_size

                            data = conn.recv(size)  # 多次接收内容，接收大数据
                            data_len = len(data)
                            received_size += data_len
                            print("已接收：%.2f" % (received_size / file_size * 100), "%")

                            m.update(data)
                            f.write(data)

                        f.close()

                        print("实际接收的大小:", received_size)  # 解码

                        # 3.md5值校验
                        md5_sever = conn.recv(1024).decode("utf-8")
                        md5_client = m.hexdigest()
                        print("服务器发来的md5:", md5_sever)
                        print("接收文件的md5:", md5_client)
                        if md5_sever == md5_client:
                            print("MD5值校验成功")
                        else:
                            print("MD5值校验失败")

                        # 3.1 确认接受
                        conn.send("准备好接收".encode('utf-8'))

                        # 4. md5值再次检验
                        md5_sever = conn.recv(1024).decode("utf-8")
                        md5_client = m.hexdigest()
                        print("服务器发来的md5:", md5_sever)
                        print("接收文件的md5:", md5_client)
                        if md5_sever == md5_client:
                            print("MD5值校验成功")

                        else:
                            print("MD5值校验失败")

    f_server.close()


# 将文件名分割出来，只留下文件名列表
def filenamee(fileString):
    pathlist1 = fileString.split('+', 1)
    pathFront = pathlist1[0]
    pathFront_tmp = pathFront[1: -1]
    path_list2 = pathFront_tmp.split('\'')
    # print(path_list2)
    return path_list2


# 多线程开启两个函数，同时启动
threading.Thread(target=thrift_server).start()
threading.Thread(target=file_server).start()
