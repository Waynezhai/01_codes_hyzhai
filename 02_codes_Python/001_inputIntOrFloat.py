#!/usr/bin/env python
#-*- coding:utf8 -*-
################################################################# 
# FileName: 001_inputIntOrFloat.py
# Author: Wayne_zhy
# Mail: zhyzhaihuiyan@163.com
# Created Time: 2019-07-11 14:54:33
# Last Modified: 2019-07-11 15:39:56
################################################################# 

def input_num():
    print "请输入一个整数或浮点数 num：",
    while True:
        num = raw_input()
        if num.replace('.', '', 1).isdigit():
            if "." in num:
                return float(num)
            else:
                return int(num)
        else:
            print "输入出错了,请重新输入：",

if __name__ == "__main__":
    num = input_num()
    print "您输入的数字 num 为：%s" % num
    print "num 的类型是 %s" % str(type(num)).split(" ")[1].split("'")[1]
