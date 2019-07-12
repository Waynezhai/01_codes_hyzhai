#!/usr/bin/env python
#-*- coding:utf8 -*-
################################################################# 
# FileName: 003_003_backupDirTool.py
# Author: Wayne_zhy
# Mail: zhyzhaihuiyan@163.com
# Created Time: 2019-07-11 16:21:49
# Last Modified: 2019-07-12 13:23:07
################################################################# 

import getopt
import sys
import os
import time


src_dir = "/tmp"
dst_dir = "./"


def usage():
    print 'Usage:\n' \
            ' -h, --help: print help message. \n' \
            ' -v, --version: print script version.\n' \
            ' -s, --src_dir: the directory which will be backuped. The src_dir is /tmp by default.\n' \
            ' -d, --dst_dir: the directory which will be backuped into. The dst_dir is ./ by default.\n' \
            ''
    sys.exit()


def version():
    print "Version: 1.0.1"
    sys.exit()


def backup(src_dir, dst_dir):
    if dst_dir.endswith(os.sep):
        dst_dir = dst_dir[0:-len(os.sep)]
    dir_today =dst_dir + os.sep + time.strftime("%Y%m%d") + "_bak"
    if not os.path.exists(dir_today):
        os.mkdir(dir_today)
        print "Created the directory %s sucessfully !" % dir_today
    target =dir_today + os.sep + time.strftime("%H%M%S") + "_bak.tar.gz"
    tar_command = "tar -zcvf {0} {1} 1> /dev/null 2> /dev/null".format(target, src_dir)
    if os.system(tar_command) == 0:
        print "Backup %s to %s sucessfully !" %(src_dir, target)
    else:
        print "Backup Failed !"


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvs:d:", ["help", "version", "src_dir=", "dst_dir="])
        #if len(opts) == 0:
        #    usage()
        for name, value in opts:
            if name in ('-h', '--help'):
                usage()
            elif name in ('-v', '--version'):
                version()
            elif name in ('-s', '--src_dir'):
                src_dir = value
                if not os.path.exists(src_dir):
                    print "The src_dir does not exist.\n" \
                            "Please check it !"
                    sys.exit()
            elif name in ('-d', '--dst_dir'):
                dst_dir = value
                if not os.path.exists(dst_dir):
                    print "The dst_dir does not exist.\n" \
                            "Please create it at first !"
                    sys.exit()
    except getopt.GetoptError:
        usage()

    backup(src_dir, dst_dir)







