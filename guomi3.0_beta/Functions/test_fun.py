#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_fun.py
# @Author: Hu Zhu
# @Date  : 7/16

import tkinter as tk
import time
import threading
from fun_sum import entry


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.createUI()

        # 生成界面

    def createUI(self):
        self.text = tk.Text(self)
        self.text.pack()

        tk.Button(self, text='加密', command=lambda: self.thread_it(self.entrya())).pack(expand=True,
                                                                                       side=tk.RIGHT)  # 注意lambda语句的作用！
        tk.Button(self, text='取消', command=lambda: self.thread_it(self.cancel)).pack(expand=True, side=tk.LEFT)

        # 逻辑：听音乐

    def music(self):
        for x in songs:
            self.text.insert(tk.END, "听歌曲：%s \t-- %s\n" % (x, time.ctime()))
            print("听歌曲：%s \t-- %s" % (x, time.ctime()))
            time.sleep(3)

        # 逻辑：看电影

    def entrya(self):
        entry('F:\\Internship\\testfile\\11\\xswlEncrypted.txt', 'F:/Internship/20190710', 0)

    def cancel(self):
        self.createUI()
    def movie(self, films):
        for x in films:
            self.text.insert(tk.END, "看电影：%s \t-- %s\n" % (x, time.ctime()))
            print("看电影：%s \t-- %s" % (x, time.ctime()))
            time.sleep(5)

        # 打包进线程（耗时的操作）

    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args)
        # t.setDaemon(True)  # 守护--就算主界面关闭，线程也会留守后台运行（不对!）
        t.start()  # 启动
        t.join()          # 阻塞--会卡死界面！


app = Application()
app.mainloop()
