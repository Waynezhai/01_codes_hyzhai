#!/usr/bin/env python
#-*- coding:utf8 -*-
################################################################# 
# FileName: 003_003_backupDirTool.py
# Author: Wayne_zhy
# Mail: zhyzhaihuiyan@163.com
# Created Time: 2019-07-11 16:21:49
# Last Modified: 2019-07-12 17:55:36
################################################################# 

"""
功能：
    在dst_dir目录下创建“%Y%m%d_bak”，目录
    把src_dir文件夹压缩后备份到目录“%Y%m%d_bak”下，压缩后的文件以“%H%M%S_bak.tar.gz”命名
思路：
    1、src_dir、dst_dir支持外部传参
    2、判断备份目录存不存在，如果不存在则创建
    3、组织备份命令，并判断执行命令返回值，如果是0则打印备份成功。如果是1则返回备份失败
说明：
    1、str.endswith("x")---判断str是否以“x”结尾，返回bool
    2、os.sep---系统分隔符，linux的返回值为“/”，windows的返回值为“\\”
    3、time.strftime("%Y%m%d%H%M%S")---获取系统时间，返回字符串
    4、os.mkdir("x")---创建文件夹x
    5、os.system(command)---执行command命令，无错误产生返回值为0，有错误产生返回值为1
"""


import os
import sys
import time
import getopt


#src_dir = "/tmp"
#dst_dir = "./"


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
        if len(opts) == 0:
            usage()
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







