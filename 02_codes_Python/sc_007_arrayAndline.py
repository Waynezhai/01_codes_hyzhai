#!/usr/bin/env python
#-*- coding:utf8 -*-
################################################################# 
# FileName: sc_007_arrayAndline.py
# Author: Wayne_zhy
# Mail: zhyzhaihuiyan@163.com
# Created Time: 2019-8-26 20:04:52
# Last Modified: 2019-08-26 20:34:19
################################################################# 

"""

功能：
    将若干行转化成一列

"""

import getopt
import sys

def usage():
    print 'Usage:\n' \
            ' -h, --help: print help message. \n' \
            ' -v, --version: print script version.\n' \
            ' -f, --filename: the name of file which will be dealed.\n' \
            ' -l, --line: the number of line you want to tansfer: xxx, yyy, zzz.\n' \
            ''
    sys.exit()

def version():
    print "Version: 1.0.1"
    sys.exit()

def judge_filename(filename):
    pass

def judge_line(linex):
    pass

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvf:l:", ["help", "version", "filename=", "line="])
        if len(opts) == 0:
            usage()
        for name, value in opts:
            if name in ('-h', '--help'):
                usage()
            elif name in ('-v', '--version'):
                version()
            elif name in ('-f', '--filename'):
                filename = value
                judge_filename(filename)
            elif name in ('-t', '--line'):
                linex = name
                judge_line(linex)
    except getopt.GetoptError:
        usage()

    fx = open(filename, "r")
    for line in fx:
        line = line[:-1]
        if line == "":
            print "\n",
        else:
            print line + "\t",
    print "\n"
    fx.close





