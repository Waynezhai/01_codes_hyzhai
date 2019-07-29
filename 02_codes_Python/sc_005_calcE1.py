#!/usr/bin/env python
#-*- coding:utf8 -*-
################################################################# 
# FileName: sc_005_calcE1.py
# Author: Wayne_zhy
# Mail: zhyzhaihuiyan@163.com
# Created Time: 2019-7-29 18:42:12 
# Last Modified: 2019-07-29 22:23:56
################################################################# 

"""

功能：
思路：
说明：

"""

import getopt
import sys

algorithm_a = ""
channel_a = "000"
alg = ""

def usage():
    print 'Usage:\n' \
            ' -h, --help: print help message. \n' \
            ' -v, --version: print script version.\n' \
            ' -a, --algorithm: the algorithm such as: "hw", "lx", "itu"\n' \
            ' -c, --channel: the E1 channel such as: "111", "373"\n' \
            ''
    sys.exit()

def version():
    print "Version: 1.0.1"
    sys.exit()
    
def judge_channel(channel_a):
    j0 = len(channel_a) != 3
    j1 = not channel_a.isdigit()
    if j0 or j1:
        print "请检查 -c 参数是否准确输入。"
        sys.exit()
    a = int(channel_a[0])
    b = int(channel_a[1])
    c = int(channel_a[2])
    ja = a not in range(1, 4)
    jb = b not in range(1, 8)
    jc = c not in range(1, 4)
    if ja or jb or jc:
        print "请检查 -c 参数是否准确输入。"
        sys.exit()

def calc(channel_a, algorithm_a):
    a = int(channel_a[0])
    b = int(channel_a[1])
    c = int(channel_a[2])
    if algorithm_a == "hw":
        alg = '华为'
        out = (c-1)*7*3 + (b-1)*3 + a
    elif algorithm_a == "lx":
        alg = '朗讯'
        out = (a-1)*7*3 + (b-1)*3 + c
    elif algorithm_a == "itu":
        alg = 'ITU'
        out = (a-1)*7*3 + b + (c-1)*7
    else:
        print "请检查 -a 参数是否准确输入。"
        sys.exit()

    print "E1 通道 %s 对应的 %s 编号为：%d " %(channel_a, alg, out) 


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hva:c:", ["help", "version", "algorithm", "channel=",])
        if len(opts) == 0:
            usage()
        for name, value in opts:
            if name in ('-h', '--help'):
                usage()
            elif name in ('-v', '--version'):
                version()
            elif name in ('-a', '--algorithm'):
                algorithm_a = value
                if algorithm_a not in ["hw", "lx", "itu"]:
                    print "请准确输入 -a 参数！"
                    sys.exit()
            elif name in ('-c', '--channel'):
                channel_a = value
                judge_channel(channel_a) 

    except getopt.GetoptError:
        usage()

    if algorithm_a == "" or channel_a == "000":
        print "请准确输入 -a/-c 参数！"
        sys.exit()
    else:
        calc(channel_a, algorithm_a)
    

