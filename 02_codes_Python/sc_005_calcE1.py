#!/usr/bin/env python
#-*- coding:utf8 -*-
################################################################# 
# FileName: sc_005_calcE1.py
# Author: Wayne_zhy
# Mail: zhyzhaihuiyan@163.com
# Created Time: 2019-7-29 18:42:12 
# Last Modified: 2019-07-29 19:08:35
################################################################# 

"""

功能：
思路：
说明：

"""

import getopt
import sys


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

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvf:a:c:", ["help", "version", "filename=", "algorithm", "channel=",])
        if len(opts) == 0:
            usage()
        for name, value in opts:
            if name in ('-h', '--help'):
                usage()
            elif name in ('-v', '--version'):
                version()
            elif name in ('-f', '--filename'):
                print "The filename is %s ." % value
            elif name in ('-a', '--algorithm'):
                algorithm_a = value
            elif name in ('-c', '--channel'):
                channel_a = value
    except getopt.GetoptError:
        usage()
    
    aug =  ""
    a = int(channel_a[0])
    b = int(channel_a[1])
    c = int(channel_a[2])

    if algorithm_a == "hw":
        alg = u'华为'
        out = (c-1)*7*3 + (b-1)*3 + a
    if algorithm_a == "lx":
        alg = u'朗讯'
        out = (a-1)*7*3 + (b-1)*3 + c
    if algorithm_a == "itu":
        alg = 'ITU'
        out = (a-1)*7*3 + b + (c-1)*7

    print "E1 通道 %s 对应的 %s 编号为：%d " %(channel_a, aug, out) 





