#!/usr/bin/env python
#-*- coding:utf8 -*-
################################################################# 
# FileName: 002_moduleOfUsage.py
# Author: Wayne_zhy
# Mail: zhyzhaihuiyan@163.com
# Created Time: 2019-07-11 16:21:49
# Last Modified: 2019-08-26 20:02:36
################################################################# 

"""

功能：
    1、创建usage的模板
    2、创建传参的模板
    3、创建版本号的雏形模板
思路：
    1、用getopt模块取sys.argv得到的第二个以后的所有参数
    2、如果没有参数，就调用usage函数打印用法说明
    3、遍历参数opts，如果不符合要求，也调用usage函数打印用法说明
说明：
    1、sys.argv方法---获取执行命令的命令及参数，返回除python解释器以外的所有以空格分隔的元素组成的列表
    2、getopt.getopt方法---
        输入为参数列表、短选项（有冒号需要传值，没有冒号不需要传值）、长选项（有等号需要传值，没等号不需要传值）
        返回一个二元组，第一个元素opts是一个由（参数标志，参数值）组成的二元组的列表；第二个元素args是除选项（-和--的参数）以外的所有参数

"""

import getopt
import sys

def usage():
    print 'Usage:\n' \
            ' -h, --help: print help message. \n' \
            ' -v, --version: print script version.\n' \
            ' -f, --filename: the name of file which will be dealed.\n' \
            ' -t, --type: the type of xxx such as: xxx, yyy, zzz.\n' \
            ''
    sys.exit()

def version():
    print "Version: 1.0.1"
    sys.exit()

def judge_filename(filename):
    pass

def judge_type(typex):
    pass

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvf:t:", ["help", "version", "filename=", "type="])
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
            elif name in ('-t', '--type'):
                typex = name
                judge_type(typex)
    except getopt.GetoptError:
        usage()






