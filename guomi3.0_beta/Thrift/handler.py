#!/usr/bin/env python
# -*- coding:utf-8; -*-
from Functions import fun_sum
# import fun_sum


class InfoHandler(object):
    def __init__(self):
        pass

    def ping(self):
        print("ping!!!!")
        return 0

    def start(self, filePath, isEn):
        '''

        :param filePath:
        :param isEn:
        :return:
        '''
        # 对传来
        pathlist = filePath.split('+', 1)
        spatha = pathlist[0]
        spath_tmp = spatha[1:-1]
        cpath = pathlist[1]
        spathlist = spath_tmp.split('\'')
        for i in range(len(spathlist)):
            if 3 > len(spathlist[i]):
                pass
            else:
                # 去除首尾空格
                spathlist_tmp = spathlist[i].strip()
                # print(spathlist_tmp)
                fun_sum.entry(spathlist_tmp, cpath, isEn)
        return 0
