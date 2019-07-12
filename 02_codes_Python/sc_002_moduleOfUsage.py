#!/usr/bin/env python
#-*- coding:utf8 -*-
################################################################# 
# FileName: 002_moduleOfUsage.py
# Author: Wayne_zhy
# Mail: zhyzhaihuiyan@163.com
# Created Time: 2019-07-11 16:21:49
# Last Modified: 2019-07-12 11:51:36
################################################################# 

import getopt
import sys


channel_list = ["stm-64", "stm-16", "stm-4", "stm-1", "tug3", "tu1x", "ts"]
type_list = ["gfp_single", "gfp_vcon", "atm", "hdlc", "chdlc", "ppp", "ss7", "pcm"]


def usage():
    print 'Usage:\n' \
            ' -h, --help: print help message. \n' \
            ' -v, --version: print script version.\n' \
            ' -f, --filename: the name of file which will be dealed.\n' \
            ' -c, --channel: the rate of channel such as: stm-64, stm-16, stm-4, stm-1, tug3, tu1x, ts.\n' \
            ' -t, --type: the type of frame such as: gfp_single, gfp_vcon, atm, hdlc, chdlc, ss7, pcm.\n' \
            ''
    sys.exit()

def version():
    print "Version: 1.0.1"
    sys.exit()

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvf:c:t:", ["help", "version", "filename=", "channel=", "type="])
        if len(opts) == 0:
            usage()
        for name, value in opts:
            if name in ('-h', '--help'):
                usage()
            elif name in ('-v', '--version'):
                version()
            elif name in ('-f', '--filename'):
                print "The filename is %s ." % value
            elif name in ('-c', '--channel'):
                if value in channel_list:
                    print "The channel is %s ." % value
                else:
                    usage()
            elif name in ('-t', '--type'):
                if value in type_list:
                    print "The type is %s ." % value
                else:
                    usage()
    except getopt.GetoptError:
        usage()
