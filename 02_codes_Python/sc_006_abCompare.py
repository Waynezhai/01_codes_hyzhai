#!/usr/bin/env python
#-*- coding:utf8 -*-
################################################################# 
# FileName: sc_006_abCompare.py
# Author: Wayne_zhy
# Mail: zhyzhaihuiyan@163.com
# Created Time: 2019-07-11 16:21:49
# Last Modified: 2019-09-03 21:24:24
################################################################# 

"""

功能：
    比较ab.txt文件中的字节大小，大于某个范围的标记出来
思路：
    ls -lR --full-time |awk {'print $5,$9'} |grep -E '96*-A$|94*-B$' > ab_2930_20190829.txt
说明：

"""

import getopt
import sys
import os

def usage():
    print 'Usage:\n' \
            ' -h, --help: print help message. \n' \
            ' -v, --version: print script version.\n' \
            ' -f, --filename: the file of ab size.\n' \
            ' -d, --dvalue: the D-value of file a and file b, the Unit is bytes.\n' \
            " do this at first: ls -lR --full-time |awk {'print $5,$9'} |grep -E '*-A$|*-B$' > ab_2930_20190829.txt\n" \
            ''
    sys.exit()

def version():
    print "Version: 1.0.1"
    sys.exit()

def judge_filename(filename):
    if not os.path.exists(filename):
        print "文件不存在，请确认！"
        sys.exit()

def judge_dvalue(dvalue):
    if not dvalue.replace('.', '', 1).isdigit():
        print "差值输入错误，请确认！"
        sys.exit()

def dict_x(filename, x):
    os.system("""cat %s |grep -e "-%s$" > xxxx.txt""" % (filename, x))
    fx = open("xxxx.txt", "r")
    dict_x = {}
    content_list = []
    for line in fx:
        content_list.append(line.split()[0])
        content_list.append(line.split()[1])
        key_fix = "-".join(line.split()[1].split("-")[:-2])
        dict_x[key_fix] = content_list 
        content_list = []
    fx.close
    os.system("""rm -rf xxxx.txt""")
    return dict_x

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvf:d:", ["help", "version", "filename=", "dvalue="])
        if len(opts) == 0:
            usage()
        for name, value in opts:
            if name in ('-h', '--help'):
                usage()
            elif name in ('-v', '--version'):
                version()
            elif name in ('-f', '--filename'):
                filename = value
            elif name in ('-d', '--dvalue'):
                dvalue = value
        judge_filename(filename)
        judge_dvalue(dvalue)
    except getopt.GetoptError:
        usage()

dict_a = dict_x(filename, "A")
dict_b = dict_x(filename, "B")

list_key = []
list_onlyInA = []
list_onlyInB = []
for key in dict_a.keys():
    if key not in dict_b.keys():
        list_onlyInA.append(key)
    else:
        list_key.append(key)
for key in dict_b.keys():
    if key not in dict_a.keys():
        list_onlyInB.append(key)

print "*" * 80
print "以下文件仅在 A 中出现："
for key in list_onlyInA:
    print dict_a[key][1]

print "*" * 80
print "以下文件仅在 B 中出现："
for key in list_onlyInB:
    print dict_b[key][1]

print "*" * 80
print "以下文件大小差值大于 %s bytes:" % dvalue
flag_ok = 0
flag_no = 0
for key in list_key:
    aaaa = dict_a[key]
    bbbb = dict_b[key]
    aabb = abs(int(aaaa[0]) - int(bbbb[0]))
    if aabb <= int(dvalue):
        flag_ok += 1
    else:
        flag_no += 1
        print "%s---差值为：%d bytes---与较大值的比为：%f%%" % (aaaa[1][:-2], aabb, aabb*100.0/max(int(aaaa[0]),int(bbbb[0])))

print "*" * 80
print "文件差值小于等于 %s bytes 的文件对数为 %d ." % (dvalue, flag_ok)
print "文件差值大于 %s bytes 的文件对数为 %d ." % (dvalue, flag_no)
print "*" * 80
