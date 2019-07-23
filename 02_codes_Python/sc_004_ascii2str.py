#!/usr/bin/env python
#-*- coding:utf8 -*-
################################################################# 
# FileName: sc_004_ascii2str.py
# Author: Wayne_zhy
# Mail: zhyzhaihuiyan@163.com
# Created Time: 2019-07-11 16:21:49
# Last Modified: 2019-07-23 14:26:08
################################################################# 

"""

功能：
思路：
说明：

"""

import sys
import getopt

input_char = "323031392d30372d32322031353a32353a3234"

def usage():
    print 'Usage:\n' \
            ' -h, --help: print help message. \n' \
            ' -v, --version: print script version.\n' \
            ' -a, --ascii: input the ascii you want to transform. and you\'d better use \"\" to quote the ascii.\n' \
            ''
    sys.exit()

def version():
    print "Version: 1.0.2"
    sys.exit()

def str2hex(s):
    odata = 0;
    su =s.upper()
    for c in su:
        tmp=ord(c)
        if tmp <= ord('9') :
            odata = odata << 4
            odata += tmp - ord('0')
        elif ord('A') <= tmp <= ord('F'):
            odata = odata << 4
            odata += tmp - ord('A') + 10
    return odata
    

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hva:", ["help", "version", "ascii="])
        if len(opts) == 0:
            usage()
        for name, value in opts:
            if name in ('-h', '--help'):
                usage()
            elif name in ('-v', '--version'):
                version()
            elif name in ('-a', '--ascii'):
                input_char = value.replace(" ", "")
    except getopt.GetoptError:
        usage()

    i = 0
    output = ""
    while i < len(input_char):
        fg = input_char[i:i+2]
        fg = "0x" + fg
        fg = str2hex(fg)
        fg = chr(fg)
        output = output + fg
        i = i + 2
        
    print output




