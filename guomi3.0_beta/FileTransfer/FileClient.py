#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : fileclient.py
# @Author: Hu Zhu
# @Date  : 7/16
# 客户端

import socket
import os
import hashlib

client = socket.socket()  # 生成socket连接对象
ipaddr = input("请输入ip地址：")
# ipaddr = '172.16.4.55'
# ipaddr = '169.254.21.210'
ip_port = (ipaddr, 8081)  # 地址和端口号

client.connect(ip_port)  # 连接

print("服务器已连接")


def file_client(content):
    # while True:
    # content = input(">>")
    # content = "sget hhh.txt"
    if len(content) == 0:
        pass  # 如果传入空字符会阻塞
    if content.startswith("cget"):
        # 命令
        client.send(content.encode("utf-8"))  # 传送和接收都是bytes类型,把这个传给server

        # 1.先接收长度，建议8192
        server_response = client.recv(1024)
        file_size = int(server_response.decode("utf-8"))
        print("接收到的大小：", file_size)

        # 2.接收文件内容
        client.send("准备好接收".encode("utf-8"))  # 接收确认

        file_cget_string = content.split(" ")[1]
        file_cget_list = filenamee(file_cget_string)
        # filename = content
        print(file_cget_list)
        for i in range(len(file_cget_list)):
            if 3 > len(file_cget_list[i]):
                pass
            else:
                c_get(file_cget_list[i], file_size)
                # return file_name[i]

    if content.startswith("sget"):
        # conn,addr = client.accept()
        # 先将命令传递给server
        client.send(content.encode("utf-8"))
        cmd = content[0:4]
        fileString = content[5:]
        # cmd, fileString = content.split(" ")
        # 将多文件分开，
        print(fileString)
        file_name = filenamee(fileString)
        print(file_name)
        for i in range(len(file_name)):
            if 3 > len(file_name[i]):
                pass
            else:
                print(555666)
                print(file_name[i])
                s_get(file_name[i])

    return True


# 将文件名分割出来，只留下文件名列表
def filenamee(fileString):
    pathlist1 = fileString.split('+', 1)
    print(pathlist1)
    pathFront = pathlist1[0]
    pathFront_tmp = pathFront[1: -1]
    path_list2 = pathFront_tmp.split('\'')
    return path_list2


def s_get(filename):
    if os.path.isfile(filename):

        # 判断文件是否存在,之后开始发送文件，让服务端准备接受
        size = os.stat(filename).st_size
        client.send((str(size) + ' ').encode('utf-8'))
        print('发送的大小为：', size)
        client.recv(1024)  # 接确认
        m = hashlib.md5()
        f = open(filename, 'rb')
        for line in f:
            client.send(line)
            m.update(line)
        f.close()

        # 3发送md5 进行校验
        md5 = m.hexdigest()
        client.send(md5.encode('utf-8'))  # 发送md5
        print('md5: ', md5)

        client.recv(1024)  # 接确认

        # 4.发送md5值再次检验
        md5 = m.hexdigest()
        client.send(md5.encode('utf-8'))  # 发送md5
        print('md5: ', md5)
        return True
    return True


def c_get(filename, file_size):
    # 如果文件目录不存在，则创建该目录
    e_path = os.path.dirname(filename)
    if not os.path.exists(e_path):
        os.makedirs(e_path)
    f = open(filename, "wb")
    received_size = 0
    m = hashlib.md5()

    while received_size < file_size:
        size = 0  # 准确接收数据大小，解决粘包
        if file_size - received_size > 1024:  # 多次接收
            size = 1024
        else:  # 最后一次接收完毕
            size = file_size - received_size

        data = client.recv(size)  # 多次接收内容，接收大数据
        data_len = len(data)
        received_size += data_len
        print("已接收：%.2f"% (received_size / file_size * 100), "%")

        m.update(data)
        f.write(data)

    f.close()

    print("实际接收的大小:", received_size)  # 解码

    # 3.md5值校验
    md5_sever = client.recv(1024).decode("utf-8")
    md5_client = m.hexdigest()
    print("服务器发来的md5:", md5_sever)
    print("接收文件的md5:", md5_client)
    if md5_sever == md5_client:
        print("MD5值校验成功")
    else:
        print("MD5值校验失败")


# content = "sget 'F:/Internship/11/Dncryptedfile.txt', 'F:/Internship/11/Encryptedfile.txt', 'F:/Internship/11/server.py'"
# file_client(content)
