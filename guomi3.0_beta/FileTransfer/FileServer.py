#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : fileserver.py
# @Author: Hu Zhu
# @Date  : 7/16

# 服务器端
import socket
import os
import hashlib

server = socket.socket()
# 获取ip地址
hostname = socket.gethostname()
ipaddr = socket.gethostbyname(hostname)
print('本机ip地址为：' + str(ipaddr))
server.bind((ipaddr, 8081))  # 绑定监听端口

server.listen(5)  # 监听

print("监听开始..")

while True:
    conn, addr = server.accept()  # 等待连接

    print("conn:", conn, "\naddr:", addr)  # conn连接实例

    while True:
        data = conn.recv(1024)  # 接收
        if not data:  # 客户端已断开
            print("客户端断开连接")
            break

        print("收到的命令：", data.decode("utf-8"))
        cmd, filename = data.decode("utf-8").split(" ")
        print(cmd)
        if "cget" == cmd:
            if os.path.isfile(filename):  # 判断文件存在

                # 1.先发送文件大小，让客户端准备接收
                size = os.stat(filename).st_size  # 获取文件大小
                conn.send(str(size).encode("utf-8"))  # 发送数据长度
                print("发送的大小：", size)

                # 2.发送文件内容
                conn.recv(1024)  # 接收确认

                m = hashlib.md5()
                f = open(filename, "rb")
                for line in f:
                    conn.send(line)  # 发送数据
                    m.update(line)
                f.close()

                # 3.发送md5值进行校验
                md5 = m.hexdigest()
                conn.send(md5.encode("utf-8"))  # 发送md5值
                print("md5:", md5)
        if "sget" == cmd:
            # hhh = server.recv(1024)
            client_responce = conn.recv(1024)  # 传文件大小
            file_size = int(client_responce.decode("utf-8"))
            print("传输的文件大小为：", file_size)

            # 2 准备接受文件
            conn.send("准备好接收".encode('utf-8'))
            f = open(filename, 'wb')
            print(filename)
            received_size = 0
            m = hashlib.md5()

            while received_size < file_size:
                size = 0  # 准确接收数据大小，解决粘包
                if file_size - received_size > 1024:  # 多次接收
                    size = 1024
                else:  # 最后一次接收完毕
                    size = file_size - received_size

                data = conn.recv(size)  # 多次接收内容，接收大数据
                data_len = len(data)
                received_size += data_len
                print("已接收：", int(received_size / file_size * 100), "%")

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

server.close()

