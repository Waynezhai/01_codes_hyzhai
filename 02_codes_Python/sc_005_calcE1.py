#!/usr/bin/env python
#-*- coding:utf8 -*-
################################################################# 
# FileName: sc_005_calcE1.py
# Author: Wayne_zhy
# Mail: zhyzhaihuiyan@163.com
# Created Time: 2019-7-29 18:42:12 
# Last Modified: 2019-08-16 17:30:42
################################################################# 

"""

功能：
思路：
说明：

"""

import getopt
import sys

type_a = ""
channel_a = "000"
alg = ""
search_flag = False

def usage():
    print 'Usage:\n' \
            ' -h, --help: print help message. \n' \
            ' -v, --version: print script version.\n' \
            ' -t, --type: the type of algorithm such as: "hw", "lx", "itu"\n' \
            ' -c, --channel: the E1 channel such as: "111", "373"\n' \
            ' -s, --search: search the No. which channel match, range in [1, 63]\n' \
            ''
    sys.exit()

def version():
    print "Version: 1.1.0"
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

def judge_search(search_a):
    if int(search_a) not in range(1, 64):
        print "请检查 -s 参数是否准确输入。"
        sys.exit()

def calc(channel_a, type_a):
    a = int(channel_a[0])
    b = int(channel_a[1])
    c = int(channel_a[2])
    if type_a == "hw":
        alg = '华为'
        out = (c-1)*7*3 + (b-1)*3 + a
    elif type_a == "lx":
        alg = '朗讯'
        out = (a-1)*7*3 + (b-1)*3 + c
    elif type_a == "itu":
        alg = 'ITU'
        out = (a-1)*7*3 + b + (c-1)*7
    else:
        print "请检查 -a 参数是否准确输入。"
        sys.exit()

    print "E1 通道 %s 对应的 %s 编号为：%d " %(channel_a, alg, out) 


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvt:c:s:", ["help", "version", "type", "channel=", "search="])
        if len(opts) == 0:
            usage()
        for name, value in opts:
            if name in ('-h', '--help'):
                usage()
            elif name in ('-v', '--version'):
                version()
            elif name in ('-t', '--type'):
                type_a = value
                if type_a not in ["hw", "lx", "itu"]:
                    print "请准确输入 -t 参数！"
                    sys.exit()
            elif name in ('-c', '--channel'):
                channel_a = value
                judge_channel(channel_a) 
            elif name in ('-s', '--search'):
                search_a = value
                search_flag = True
                judge_search(search_a) 

    except getopt.GetoptError:
        usage()

    if type_a != "" and channel_a != "000":
        calc(channel_a, type_a)
    if type_a != "" and channel_a == "000":
        print " TUG3 | TUG2 | TU1x | No_%s" % type_a
        print "=" * 30
        dict_x = {}
        for a in range(1,4):
            for b in range(1,8):
                for c in range(1,4):
                    abc = str(a).center(6) + "|" + str(b).center(6) + "|" + str(c).center(6) + "|"
                    if type_a == "hw":
                        out = (c-1)*7*3 + (b-1)*3 + a
                    elif type_a == "lx":
                        out = (a-1)*7*3 + (b-1)*3 + c
                    elif type_a == "itu":
                        out = (a-1)*7*3 + b + (c-1)*7
                    dict_x[str(out)] = abc
                    if not search_flag:
                        print abc,str(out).center(6)
        if search_flag:
            print dict_x[search_a],search_a 
    

