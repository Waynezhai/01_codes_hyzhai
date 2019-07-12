#!/usr/bin/env python
#-*- coding:utf8 -*-
################################################################# 
# FileName: 001_inputIntOrFloat.py
# Author: Wayne_zhy
# Mail: zhyzhaihuiyan@163.com
# Created Time: 2019-07-11 14:54:33
# Last Modified: 2019-07-12 14:45:05
################################################################# 
"""

功能：
    校验输入的是一个整数或浮点数
说明：
    1、str.replace("a", "b", 5)---return a str---字符串str中的前 5 个 a 用 b来代替；5 可以省略，省略表示将所有 a 用 b 替换
    2、str.isdigit()---return a bool---字符串str中的所有字符都是数字
    3、str.split("x")---return a list---字符串str被字符“x”分割后的字符组成的列表

"""
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
