#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : surface.py
# @Author: Hu Zhu
# @Date  : 7/16
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import askdirectory
from tkinter import scrolledtext
import tkinter.messagebox as messagebox
import tkinter as tk
from tkinter import *
import time
from Thrift import client
import threading
from FileTransfer.FileClient import file_client
from FileOperate.exfilename import ExFileName

sender = client.client.create()


class MainInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.openpath = StringVar()  # 获取选择文件路径
        self.savepath = StringVar()  # 获取保存文件路径
        self.mUItext1 = ''
        self.mUItext2 = ''
        self.mainUI()  # 主界面

    def interface_info(self):  # 主界面大小
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - 200
        y = (hs / 2) - 200
        return x, y

    def mainUI(self):
        self.title("加密解密")
        a, b = self.interface_info()
        self.geometry("600x300+%d+%d" % (a, b))

        self.mUItext1 = scrolledtext.ScrolledText(self, width=40, height=5)  # 主界面上的那俩框
        self.mUItext1.grid(row=1, column=3, rowspan=8, stick=W, pady=5, padx=5)
        self.mUItext2 = scrolledtext.ScrolledText(self, width=40, height=5)
        self.mUItext2.grid(row=20, column=3, rowspan=8, stick=W, pady=8, padx=5)
        Label(self, text="初始文件：").grid(row=4, column=0)
        Label(self, text="已处理文件:").grid(row=25, column=0)
        tk.Label(self, text="初始文件：")  # .grid(row=4, column=0)
        tk.Label(self, text="已处理文件:")  # .grid(row=25, column=0)
        tk.Button(self, text='加密', command=lambda: self.thread_it(self.encrypt)).grid(row=4, column=5, pady=10,
                                                                                      padx=10)  # stick=E+W
        tk.Button(self, text='解密', command=lambda: self.thread_it(self.decode)).grid(row=25, column=5, pady=5,
                                                                                     padx=5)  # stick=E+W
        tk.Button(self, text='取消', command=lambda: self.thread_it(self.cancel)).grid(row=30, column=5, pady=5,
                                                                                     padx=5)  # stick=E+W

    def encrypt(self):  # 点了加密后的界面
        sender.ping()
        top = tk.Toplevel()
        top.title('加密')

        def ensureencrypt():  # 确定文件路径、文件类型是否正确，文件路径是否完整，正确后开始加密
            if self.filepath() and self.allpath():
                top.destroy()  # 关闭子界面
                print("开始传输文件以及加密过程")
                content_sget = 'sget ' + PassAddress
                # 开始加密
                sender.ping()
                if file_client(content_sget):
                    self.thread_it(sender.start(PassAddress, 1))

                # 加密结束后，开始回传，注意回传的路径
                out_path = PathString(PassAddress, 1)
                file_client(out_path)

                self.thread_it(self.progressbar())  # 进度条
                return True
            else:
                return False

        # 加密子界面部件
        Label(top, text="选择文件:").grid(row=0, column=0)
        Button(top, text="浏览", command=self.choosepic).grid(row=0, column=2)
        Label(top, text="保存文件:").grid(row=1, column=0)
        Label(top, textvariable=self.openpath, bg='white', width=20).grid(row=0, column=1)  # 加密子界面选择文件文本框里的内容
        Label(top, textvariable=self.savepath, bg='white', width=20).grid(row=1, column=1)  # 加密子界面保存文件文本框里的内容
        Button(top, text="浏览", command=self.save).grid(row=1, column=2)
        Button(top, text="确定", command=ensureencrypt).grid(row=2, column=2, pady=5,
                                                           padx=5)  # stick=E+W

    def decode(self):  # 点了解密后的界面
        top = Toplevel()
        top.title('解密')

        def ensuredecode():  # 确定文件路径、文件类型是否正确，文件路径是否完整，正确后开始加密
            if self.filepath() and self.allpath():
                top.destroy()  # 关闭子界面
                print('I am in decrypting')
                content_sget = 'sget ' + PassAddress
                # 开始加密
                sender.ping()
                if file_client(content_sget):
                    self.thread_it(sender.start(PassAddress, 0))
                out_string = PathString(PassAddress, 0)
                file_client(out_string)
                self.thread_it(self.progressbar())  # 进度条
                return True
            else:
                return False

        # 解密界面部件
        Label(top, text="选择文件:").grid(row=0, column=0)
        Button(top, text="浏览", command=self.choosepic).grid(row=0, column=2)
        Label(top, text="保存文件:").grid(row=1, column=0)
        Label(top, textvariable=self.openpath, bg='white', width=20).grid(row=0, column=1)  # 加密子界面选择文件文本框里的内容
        Label(top, textvariable=self.savepath, bg='white', width=20).grid(row=1, column=1)  # 加密子界面保存文件文本框里的内容
        Button(top, text="浏览", command=self.save).grid(row=1, column=2)
        Button(top, text="确定", command=ensuredecode).grid(row=2, column=2, pady=5, padx=5)  # stick=E+W

    def choosepic(self):  # 选择文件
        path_ = askopenfilenames()
        strpath_ = str(path_)
        self.openpath.set(path_)
        self.mUItext1.insert("insert", '选择文件：')  # 主界面选择文件文本框里的内容
        self.mUItext1.insert("insert", path_)
        self.mUItext1.insert("insert", '\n')
        # print(strpath_)
        return path_

    def filepath(self):  # 判断路径是否输入完整
        openPath = self.openpath.get()
        savePath = self.savepath.get()
        if openPath and savePath:
            return True
        else:
            messagebox.showerror(title='Wrong inputs!', message='文件路径出错.')  # 错误提示对话框
            return False

    def allpath(self):  # 连接打开与保存路径
        # 将地址变成string型
        openPath = self.openpath.get()
        savePath = self.savepath.get()
        global PassAddress
        PassAddress = '+'.join([openPath, savePath])
        print("需要加密的文件为：" + PassAddress)
        return PassAddress

    def save(self):  # 保存文件
        path = askdirectory()
        self.mUItext2.insert("end", '处理后的文件：')  # 主界面保存文件文本框里的内容
        self.mUItext2.insert("end", path)
        self.savepath.set(path)
        print("保存的路径为：" + path)
        return path

    def progressbar(self):  # 进度条
        def change_schedule(now_schedule, all_schedule):  # 进度条更新函数
            canvas.coords(fill_rec, (5, 5, 6 + (now_schedule / all_schedule) * 100, 25))
            self.update()
            num.set(str(round(now_schedule / all_schedule * 100, 2)) + '%')
            if round(now_schedule / all_schedule * 100, 2) == 100.00:
                num.set("完成")

        # 创建画布
        frame = Frame().grid(row=3, column=4)  # 使用时将框架根据情况选择新的位置
        canvas = Canvas(frame, width=120, height=30, bg="white")
        canvas.grid(row=40, column=5)
        num = StringVar()

        # 进度条以及完成程度
        out_rec = canvas.create_rectangle(5, 5, 105, 25, outline="blue", width=1)
        fill_rec = canvas.create_rectangle(5, 5, 5, 25, outline="", width=0, fill="blue")
        Label(frame, textvariable=num).grid(row=40, column=6)
        for i in range(100):
            time.sleep(0.01)
            change_schedule(i, 99)
        messagebox.showinfo(title='Finish!', message='操作成功.')

    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)  # 守护--就算主界面关闭，线程也会留守后台运行（不对!）
        t.start()  # 启动
        # t.join()          # 阻塞--会卡死界面！


# 将加密后的文件回传
def PathString(PassAddress, isEn):
    # 对传来
    ENSTRING = "Encrypted"
    DESTRING = "Decrypted"
    out_string1 = ''
    # out_string = ''
    pathlist = PassAddress.split('+', 1)
    spathb = pathlist[1]  # 保存的文件夹
    spatha = pathlist[0]
    spath_tmp = spatha[1:-1]  # 文件路径的东西
    # cpath = pathlist[1]
    spathlist = spath_tmp.split('\'')
    for i in range(len(spathlist)):
        if 3 > len(spathlist[i]):
            pass
        else:
            # 去除首尾空格
            spathlist_tmp = spathlist[i].strip()  # 需要进行操作的文件的绝对路径
            spathlist_tmp_e = ExFileName(spathlist_tmp).extension_filenm()  # 提取了文件后缀名
            spathlist_tmp_f = ExFileName(spathlist_tmp).ex_front_filenm()  # 不带后缀的名字
            if 1 == isEn:  # 加密
                out_string1 += "('" + spathb + "/" + spathlist_tmp_f + ENSTRING + spathlist_tmp_e + "')"
            elif 0 == isEn:
                out_string1 += "('" + spathb + "/" + spathlist_tmp_f + DESTRING + spathlist_tmp_e + "')"
    out_string = "cget " + out_string1
    return out_string


app = MainInterface()
app.mainloop()
