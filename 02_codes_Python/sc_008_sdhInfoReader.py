#!/usr/bin/env python
#-*- coding:utf8 -*-
################################################################# 
# FileName: sdh_info_reader.py
# Author: Wayne_zhy
# Mail: zhyzhaihuiyan@163.com
# Created Time: 2019-07-11 16:21:49
# Last Modified: 2019-09-17 00:02:41
################################################################# 

"""

功能：
    1、对sdh_info文件进行解读，分析出哪些速率通道中有哪些成帧类型
    2、支持通道速率有："stm-64", "stm-16", "stm-4", "stm-1", "tug3", "tu1x", "ts"
    3、支持成帧类型有："gfp_single", "gfp_vcon", "atm", "hdlc", "chdlc", "ppp", "ss7", "pcm", "all"
    4、如果带参数all的话，则把所有通道速率的所有成帧类型都分析出来
思路：

"""

import os
import sys
import getopt
import linecache

filename_a = ""
abstract_a = ""
channel_a = ""
type_a = ""


def usage():
    print 'Usage:\n' \
            ' -h, --help: print help message. \n' \
            ' -v, --version: print script version.\n' \
            ' -f, --filename: the name of file which will be dealed.\n' \
            ' -a, --abstract: print the abstrcat of the link which in the sdh_info. The input would be in: stm-x, tugx, tu1x, ts.\n' \
            ' -c, --channel: the rate of channel such as: stm-64, stm-16, stm-4, stm-1, tug3, tug2, tu1x, ts.\n' \
            ' -t, --type: the type of frame such as: pos, null, tug2s, gfp_s, gfp_v, atm, hdlc, chdlc, ppp, ss7, pcm, fr.\n' \
            ''
    sys.exit()

def version():
    print "Version: 1.0.1"
    sys.exit()

def filename_check(filename_a):
    if not os.path.exists(filename_a):
        print "The file you input does not exist."
        sys.exit()
    
def abstract_check(abstract_a):
    return
    abstract_list = ["", "stm-x", "tugx", "tu1x", "ts"]
    if abstract_a not in abstract_list:
        print "You should input the exact level such as: stm-x, tugx, ts."
        sys.exit()

def channel_check(channel_a):
    return
    channel_list = ["", "stm-64", "stm-16", "stm-4", "stm-1", "tug3", "tug2", "tu1x", "ts"]
    if channel_a not in channel_list:
        print "The channel you input is wrong. Please check it."
        sys.exit()

def type_check(type_a):
    return
    type_list = ["", "pos", "null", "tug2s", "E1", "gfp_s", "gfp_v", "gfp", "atm", "hdlc", "chdlc", "ppp", "ss7", "pcm", "fr"]
    if type_a not in type_list:
        print "The type you input is wrong. Please check it."
        sys.exit()

# 记录stm-x所在行，并把行号、stm-x所在行、stm-x所在行的下一行存在 line_stmX 中返回
def line_stmX_pop(filename_a):
    fn = open(filename_a, 'r')
    line_num = 1
    line_stmX = []
    for line in fn:
        if "stmx:" in line:
            line_stmX.append([line_num, line])
        line_num += 1
    fn.close
    for index in range(len(line_stmX)):
        line_num = int(line_stmX[index][0]) + 1
        line_add = linecache.getline(filename_a, line_num)
        line_stmX[index].append(line_add)
    return line_stmX

# 从stm-x的下一行中提取所有的 stm-x 级别的通道类型，包括 TUG3 和 null
def stmX_type_set_pop(line_stmX):
    stmX_type_set = set()
    for index in range(len(line_stmX)):
        if line_stmX[index][2].strip().split()[0] != "[TUG3]":
            stmX_type_set.add(line_stmX[index][2].strip().split()[0][7:])
        else:
            stmX_type_set.add("TUG3")
    return stmX_type_set

# 通过判断最后一个stm-x行的内容来确定接入纤的速率等级，如“ch:49 stmx:16”
def rate_identify(line_stmX):
    rate = int(line_stmX[-1][1].split()[1][3:]) + int(line_stmX[-1][1].split()[2][5:]) - 1
    if rate == 1:
        print "接入链路的速率为: 155M_SDH."
    elif rate == 4:
        print "接入链路的速率为: 622M_SDH."
    elif rate == 16:
        print "接入链路的速率为: 2.5G_SDH."
    elif rate == 64:
        print "接入链路的速率为: 10G_SDH"
    else:
        print "sdh_info文件异常，请检查！"

# 粗略判断接入链路中有多少个stm-x，展示出所有的相邻级联成分
def stmx_thick(line_stmX, stmX_type_set):
    num_stm64 = 0
    num_stm16 = 0
    num_stm4 = 0
    num_stm1 = 0
    stmx_dict = {"64":num_stm64, "16":num_stm16, "4":num_stm4, "1":num_stm1}
    for index in range(len(line_stmX)):
        if line_stmX[index][1].split()[2][5:] in stmx_dict.keys():
            stmx_dict[line_stmX[index][1].split()[2][5:]] += 1
    num_stm64 = stmx_dict["64"]
    num_stm16 = stmx_dict["16"]
    num_stm4 = stmx_dict["4"]
    num_stm1 = stmx_dict["1"]
    print "链路中有：\n" \
            "\tstm-64 %d 条；stm-16 %d 条；stm-4 %d 条；stm-1 %d 条。" % (num_stm64, num_stm16, num_stm4, num_stm1)

# 对stm-x进行精细分析，找出每个stm-x中都有什么成分
def stmx_thin(line_stmX, stmX_type_set):
    type_list = list(stmX_type_set)
    mark_stm64 = {}
    mark_stm16 = {}
    mark_stm4 = {}
    mark_stm1 = {}
    mark_all = {"stm-64":mark_stm64, "stm-16":mark_stm16, "stm-4":mark_stm4, "stm-1":mark_stm1}
    for index in range(len(type_list)):
        mark_stm64[type_list[index]] = 0
        mark_stm16[type_list[index]] = 0
        mark_stm4[type_list[index]] = 0
        mark_stm1[type_list[index]] = 0
    for index in range(len(line_stmX)):
        if line_stmX[index][1].split()[2][5:] == "64":
            if line_stmX[index][2].strip().split()[0] != "[TUG3]":
                mark_stm64[line_stmX[index][2].strip().split()[0][7:]] += 1
            else:
                mark_stm64["TUG3"] += 1
        if line_stmX[index][1].split()[2][5:] == "16":
            if line_stmX[index][2].strip().split()[0] != "[TUG3]":
                mark_stm16[line_stmX[index][2].strip().split()[0][7:]] += 1
            else:
                mark_stm16["TUG3"] += 1
        if line_stmX[index][1].split()[2][5:] == "4":
            if line_stmX[index][2].strip().split()[0] != "[TUG3]":
                mark_stm4[line_stmX[index][2].strip().split()[0][7:]] += 1
            else:
                mark_stm4["TUG3"] += 1
        if line_stmX[index][1].split()[2][5:] == "1":
            if line_stmX[index][2].strip().split()[0] != "[TUG3]":
                mark_stm1[line_stmX[index][2].strip().split()[0][7:]] += 1
            else:
                mark_stm1["TUG3"] += 1
    for mark_stmX in mark_all.values():
        for key in mark_stmX.keys():
            if mark_stmX[key] == 0:
                mark_stmX.pop(key)
    for key in mark_all.keys():
        if mark_all[key] == {}:
            mark_all.pop(key)
        else:
            pass

    # 给 stm-x 排序。x 越大，越靠前
    list_tmp = mark_all.keys()
    dict_tmp = {}
    for index in range(len(list_tmp)):
        x = int(list_tmp[index][4:])
        dict_tmp[x] = list_tmp[index]
    set_tmp = sorted(dict_tmp.items(),reverse=True)
    list_tmp = []
    for index in range(len(set_tmp)):
        list_tmp.append(set_tmp[index][1])

    print "其中："
    for key in list_tmp:
        print "\t%s 链路中有：" % key,
        last = len(mark_all[key].keys())
        for key_stmx in mark_all[key].keys():
            if last != 1:
                print "%s 结构 %s 条;" % (key_stmx, mark_all[key][key_stmx]),
            elif last == 1:
                print "%s 结构 %s 条。" % (key_stmx, mark_all[key][key_stmx]),
            else:
                print "sth is wrong！"
            last -= 1
        print ""

# 判断某一级别stm-x的类型在哪条通道，并打印出C2值，支持pos、atm、null
def channel_pan(channel_a, type_a):
    type_num = 0
    type_list = []
    for index in range(len(line_stmX)):
        if type_a == line_stmX[index][2].split()[0][7:]:
            if channel_a[4:] == line_stmX[index][1].split()[2][5:]:
                type_index = []
                type_index.append(line_stmX[index][1].split()[1][3:])
                type_index.append(line_stmX[index][1].split()[4][3:])
                type_list.append(type_index)
                type_num += 1
    print "%s 链路中，共有 %s 链路 %d 条。" % (channel_a, type_a, type_num)
    for index in range(0,type_num):
        if channel_a != "stm-1":
            print "\t第 %s 条 %s 的通道起始编号为 %s, C2值为 %s。" % (index+1, type_a, type_list[index][0], type_list[index][1])
        else:
            print "\t第 %s 条 %s 的通道编号为 %s, C2值为 %s。" % (index+1, type_a, type_list[index][0], type_list[index][1])

def gfp_check(channel_a, type_a):
    if channel_a == "stm-1":
        gid_list = []
        gid_set = set()
        gid_dict = {}
        # 遍历 stm-x 所在行的下一行中的 framer字段，如果是gfp，就把整个元素存在gid_list中
        # 并把 gid 存在一个集合 gid_set 中
        # 再创立一个字典，键为gid，值为gid出现的次数，这样就可以方便地区分是单stm-1的gfp还是虚级联的gfp了
        for index in range(len(line_stmX)):
            gfp_flag = line_stmX[index][2].split()[0]
            if gfp_flag == "framer:gfp":
                gid_list.append(line_stmX[index])
                gid_tmp = line_stmX[index][2].split()[-1][4:]
                if gid_tmp in gid_set:
                    gid_dict[gid_tmp] += 1
                else:
                    gid_dict[gid_tmp] = 1
                    gid_set.add(gid_tmp)
        #print gid_set
        #print gid_dict
        # 如果是单stm-1通道的gfp，就用gid遍历gid_list，取出通道哦值即可
        if type_a == "gfp_s":
            print "stm-1级别的单 gfp 通道有："
            for key in gid_dict.keys():
                if gid_dict[key] == 1:
                    for index in range(len(gid_list)):
                        if gid_list[index][2].split()[-1][4:] == key:
                            print "\tgid 为 %s，通道 ID 为 %s" % (key, gid_list[index][1].split()[1][3:])
        # 如果是多stm-1虚级联的gfp，就遍历gid_list，把一个gid的不同stm-1的 vsn/ctrl/channel 三个字段存到一个列表中
        # 在把一个组的[vsn, ctrl, channel]存放到一个虚级联列表 gid_vc_list 中
        elif type_a == "gfp_v":
            print "stm-1级别的 gfp 虚级联通道有："
            for key in gid_dict.keys():
                if gid_dict[key] != 1:
                    print "\tgid 为 %s 的虚级联分组的 Channel_id 为：" % key,
                    gid_vc_list = []
                    for index in range(len(gid_list)):
                        gid_vc_atom = []
                        if gid_list[index][2].split()[-1][4:] == key:
                            gid_vc_atom.append(gid_list[index][2].split()[3][4:])   # vsn
                            gid_vc_atom.append(gid_list[index][2].split()[4][5:])   # ctrl
                            gid_vc_atom.append(gid_list[index][1].split()[1][3:])   # channel
                            gid_vc_list.append(gid_vc_atom)
                            #print "\t\t",gid_list[index]
                    # 把一个虚级联组的 vsn 单独取出来存到列表中排序
                    vsn_list = []
                    for index in range(len(gid_vc_list)):
                        vsn_list.append(gid_vc_list[index][0])
                    vsn_list.sort()
                    # 按照排过序的额 vsn 打印 channel_id
                    for index in range(len(vsn_list)):
                        for indexX in range(len(gid_vc_list)):
                            if vsn_list[index] == gid_vc_list[indexX][0]:
                                if index != len(vsn_list)-1:
                                    print gid_vc_list[indexX][2] + ",",
                                elif index == len(vsn_list)-1:
                                    print gid_vc_list[indexX][2] + " ---",
                    # 判断 vsn 是否正常，如果一个虚级联组的最后一个 vsn_id 等于vsn个数减1，那么认为是正常的
                    if int(vsn_list[-1]) == len(vsn_list) - 1:
                        print "vsn 连续 ---",
                    else:
                        print "vsn 不连续 ---",
                    # 判断 ctrl_id 是否正常，如果前序 ctrl_id 为 2，最后一个 ctrl_id 为 3，那么认为是正常的
                    ctrl_flag = True
                    for index in range(len(gid_vc_list)):
                        if gid_vc_list[index][0] == vsn_list[0]:
                            if gid_vc_list[index][1] == "2":
                                pass
                            else:
                                ctrl_flag = False
                        if gid_vc_list[index][0] == vsn_list[-1]:
                            if gid_vc_list[index][1] == "3":
                                pass
                            else:
                                ctrl_flag = False
                    if ctrl_flag == True:
                        print "ctrl_id 字段正常。"
                    else:
                        print "ctrl_id 字段异常。"
        else:
            print "sth is wrong !"
            

def line_tugX_pop(filename_a):
    fn = open(filename_a, 'r')
    line_num = 1
    line_tugX = []
    for line in fn:
        if "[TUG3] ch" in line:
            line_tugX.append([line_num, line])
        line_num += 1
    fn.close
    #print line_tugX
    for index in range(len(line_tugX)):
        list_stm1 = [""]
        for inde_X in range(len(line_stmX)):
            if line_tugX[index][0] - line_stmX[inde_X][0] > 0:
                list_stm1.pop()
                list_stm1.append(line_stmX[inde_X][:-1])
            else:
                break
        #print list_stm1
        line_tugX[index].append(list_stm1[-1])
    return line_tugX

def tugX_type_set_pop(line_tugX):
    tugX_type_set = set()
    for index in range(len(line_tugX)):
        if line_tugX[index][1].split()[2][7:] != "":
            tugX_type_set.add(line_tugX[index][1].split()[2][7:])
        elif line_tugX[index][1].split()[3] == "tug2s":
            tugX_type_set.add("tug2s")
        else:
            print line_tugX[index]
    return tugX_type_set


def tugx_thick(line_tugX, tugX_type_set):
    type_list = list(tugX_type_set)
    mark_tugX = {}
    for index in range(len(type_list)):
        mark_tugX[type_list[index]] = 0
    for index in range(len(type_list)):
        for inde_X in range(len(line_tugX)):
            if type_list[index] in line_tugX[inde_X][1]:
                mark_tugX[type_list[index]] += 1
    #print mark_tugX
    print "TUG3 链路中有：\n\t",
    for key in mark_tugX.keys():
        if key != mark_tugX.keys()[-1]:
            print "%s 链路 %d 条；" % (key, mark_tugX[key]),
        if key == mark_tugX.keys()[-1]:
            print "%s 链路 %d 条。" % (key, mark_tugX[key])


def channel_thn(channel_a, type_a):
    type_num = 0
    type_list = []
    if type_a == "tug2s":
        for index in range(len(line_tugX)):
            if line_tugX[index][1].split()[3] == "tug2s":
                type_list.append(line_tugX[index])
                type_num += 1
    else:
        for index in range(len(line_tugX)):
            if line_tugX[index][1].split()[2][7:] == type_a:
                type_list.append(line_tugX[index])
                type_num += 1
    print "TUG3 链路中，共有 %s 链路 %d 条。" % (type_a, type_num)
    for index in range(0,type_num):
        ch_id = type_list[index][2][1].split()[1][3:] + "_" + type_list[index][1].split()[1][3:]
        if index != type_num-1:
            print "\t第 %s 条 %s 的通道编号为 %s；" % (index+1, type_a, ch_id)
        else:
            print "\t第 %s 条 %s 的通道编号为 %s。" % (index+1, type_a, ch_id)

def gfp_tug3_check(channel_a, type_a):
    if channel_a == "tug3":
        gid_list = []
        gid_set = set()
        gid_dict = {}
        # 遍历 TUG3 所在行的下一行中的 framer字段，如果是gfp，就把整个元素存在gid_list中
        # 并把 gid 存在一个集合 gid_set 中
        # 再创立一个字典，键为gid，值为gid出现的次数，这样就可以方便地区分是单TUG3的gfp还是虚级联的gfp了
        for index in range(len(line_tugX)):
            gfp_flag = line_tugX[index][1].split()[2]
            if gfp_flag == "framer:gfp":
                gid_list.append(line_tugX[index])
                gid_tmp = line_tugX[index][1].split()[-1][4:]
                if gid_tmp in gid_set:
                    gid_dict[gid_tmp] += 1
                else:
                    gid_dict[gid_tmp] = 1
                    gid_set.add(gid_tmp)
        #print gid_list
        #print gid_set
        #print gid_dict
        # 如果是单TUG3通道的gfp，就用gid遍历gid_list，取出通道值，并在前面加上STM-1的信息
        if type_a == "gfp_s":
            print "TUG3 级别的单 gfp 通道有："
            for key in gid_dict.keys():
                if gid_dict[key] == 1:
                    for index in range(len(gid_list)):
                        if gid_list[index][1].split()[-1][4:] == key:
                            ch_id = gid_list[index][2][1].split()[1][3:] + "_" + gid_list[index][1].split()[1][3:]
                            print "\tgid 为 %s，通道 ID 为 %s" % (key, ch_id)
        # 如果是多TUG3虚级联的gfp，就遍历gid_list，把一个gid的不同stm-1的 vsn/ctrl/channel 三个字段存到一个列表中
        # 在把一个组的[vsn, ctrl, channel]存放到一个虚级联列表 gid_vc_list 中
        elif type_a == "gfp_v":
            print "TUG3 级别的 gfp 虚级联通道有："
            for key in gid_dict.keys():
                if gid_dict[key] != 1:
                    print "\tgid 为 %s 的虚级联分组的 Channel_id 为：" % key,
                    gid_vc_list = []
                    for index in range(len(gid_list)):
                        gid_vc_atom = []
                        if gid_list[index][1].split()[-1][4:] == key:
                            gid_vc_atom.append(gid_list[index][1].split()[5][4:])   # vsn
                            gid_vc_atom.append(gid_list[index][1].split()[6][5:])   # ctrl
                            ch_id = gid_list[index][2][1].split()[1][3:] + "_" + gid_list[index][1].split()[1][3:]
                            gid_vc_atom.append(ch_id)   # channel
                            gid_vc_list.append(gid_vc_atom)
                            #print "\t\t",gid_list[index]
                    # 把一个虚级联组的 vsn 单独取出来存到列表中排序
                    vsn_list = []
                    for index in range(len(gid_vc_list)):
                        vsn_list.append(gid_vc_list[index][0])
                    vsn_list.sort()
                    # 按照排过序的额 vsn 打印 channel_id
                    for index in range(len(vsn_list)):
                        for indexX in range(len(gid_vc_list)):
                            if vsn_list[index] == gid_vc_list[indexX][0]:
                                if index != len(vsn_list)-1:
                                    print gid_vc_list[indexX][2] + ",",
                                elif index == len(vsn_list)-1:
                                    print gid_vc_list[indexX][2] + " ---",
                    # 判断 vsn 是否正常，如果一个虚级联组的最后一个 vsn_id 等于vsn个数减1，那么认为是正常的
                    if int(vsn_list[-1]) == len(vsn_list) - 1:
                        print "vsn 连续 ---",
                    else:
                        print "vsn 不连续 ---",
                    # 判断 ctrl_id 是否正常，如果前序 ctrl_id 为 2，最后一个 ctrl_id 为 3，那么认为是正常的
                    ctrl_flag = True
                    for index in range(len(gid_vc_list)):
                        if gid_vc_list[index][0] == vsn_list[0]:
                            if gid_vc_list[index][1] == "2":
                                pass
                            else:
                                ctrl_flag = False
                        if gid_vc_list[index][0] == vsn_list[-1]:
                            if gid_vc_list[index][1] == "3":
                                pass
                            else:
                                ctrl_flag = False
                    if ctrl_flag == True:
                        print "ctrl_id 字段正常。"
                    else:
                        print "ctrl_id 字段异常。"
        else:
            print "sth is wrong !"


def line_tu1X_pop(filename_a):
    fn = open(filename_a, 'r')
    line_num = 1
    line_tu1X = []
    for line in fn:
        if "[TU1x] ch:" in line:
            line_tu1X.append([line_num, line])
        line_num += 1
    fn.close
    for index in range(len(line_tu1X)):
        list_stm1 = [""]
        for inde_X in range(len(line_stmX)):
            if line_tu1X[index][0] - line_stmX[inde_X][0] > 0:
                list_stm1.pop()
                list_stm1.append(line_stmX[inde_X][:-1])
            else:
                break
        #print list_stm1
        line_tu1X[index].append(list_stm1[-1])
    #print line_tu1X
    return line_tu1X

def tu1X_type_set_pop(line_tu1X):
    tu1X_type_set = set()
    for index in range(len(line_tu1X)):
        if line_tu1X[index][1].split()[3][7:] != "":
            tu1X_type_set.add(line_tu1X[index][1].split()[3][7:])
        elif line_tu1X[index][1].split()[4] == "E1":
            tu1X_type_set.add("E1")
        else:
            print line_tu1X[index]
    return tu1X_type_set


def tu1x_thick(line_tu1X, tu1X_type_set):
    type_list = list(tu1X_type_set)
    mark_tu1X = {}
    for index in range(len(type_list)):
        mark_tu1X[type_list[index]] = 0
    for index in range(len(type_list)):
        for inde_X in range(len(line_tu1X)):
            if type_list[index] in line_tu1X[inde_X][1]:
                mark_tu1X[type_list[index]] += 1
    #print mark_tugX
    print "TU1X 链路中有：\n\t",
    for key in mark_tu1X.keys():
        if key != mark_tu1X.keys()[-1]:
            print "%s 链路 %d 条；" % (key, mark_tu1X[key]),
        if key == mark_tu1X.keys()[-1]:
            print "%s 链路 %d 条。" % (key, mark_tu1X[key])


def channel_ne1(channel_a, type_a):
    type_num = 0
    type_list = []
    if type_a == "E1":
        for index in range(len(line_tu1X)):
            if line_tu1X[index][1].split()[4] == "E1":
                type_list.append(line_tu1X[index])
                type_num += 1
    else:
        for index in range(len(line_tu1X)):
            if line_tu1X[index][1].split()[3][7:] == type_a:
                type_list.append(line_tu1X[index])
                type_num += 1
    print "TU1X 链路中，共有 %s 链路 %d 条。" % (type_a, type_num)
    for index in range(0,type_num):
        ch_id = type_list[index][2][1].split()[1][3:] + "_" + type_list[index][1].split()[2][1:-1]
        if index != type_num-1:
            print "\t第 %s 条 %s 的通道编号为 %s；" % (index+1, type_a, ch_id)
        else:
            print "\t第 %s 条 %s 的通道编号为 %s。" % (index+1, type_a, ch_id)

def gfp_tu1x_check(channel_a, type_a):
    if channel_a == "tu1x":
        gid_list = []
        gid_set = set()
        gid_dict = {}
        # 遍历 TU1X 所在行的下一行中的 framer字段，如果是gfp，就把整个元素存在gid_list中
        # 并把 gid 存在一个集合 gid_set 中
        # 再创立一个字典，键为gid，值为gid出现的次数，这样就可以方便地区分是单TU1X的gfp还是虚级联的gfp了
        for index in range(len(line_tu1X)):
            gfp_flag = line_tu1X[index][1].split()[3]
            if gfp_flag == "framer:gfp":
                gid_list.append(line_tu1X[index])
                gid_tmp = line_tu1X[index][1].split()[-1][4:]
                if gid_tmp in gid_set:
                    gid_dict[gid_tmp] += 1
                else:
                    gid_dict[gid_tmp] = 1
                    gid_set.add(gid_tmp)
        #print gid_list
        #print gid_set
        #print gid_dict
        # 如果是单TU1X通道的gfp，就用gid遍历gid_list，取出通道值，并在前面加上STM-1的信息
        if type_a == "gfp_s":
            print "TU1X 级别的单 gfp 通道有："
            for key in gid_dict.keys():
                if gid_dict[key] == 1:
                    for index in range(len(gid_list)):
                        if gid_list[index][1].split()[-1][4:] == key:
                            ch_id = gid_list[index][2][1].split()[1][3:] + "_" + gid_list[index][1].split()[2][1:-1]
                            print "\tgid 为 %s，通道 ID 为 %s" % (key, ch_id)
        # 如果是多TUG3虚级联的gfp，就遍历gid_list，把一个gid的不同stm-1的 vsn/ctrl/channel 三个字段存到一个列表中
        # 在把一个组的[vsn, ctrl, channel]存放到一个虚级联列表 gid_vc_list 中
        elif type_a == "gfp_v":
            print "TU1X 级别的 gfp 虚级联通道有："
            for key in gid_dict.keys():
                if gid_dict[key] != 1:
                    print "\tgid 为 %s 的虚级联分组的 Channel_id 为：" % key,
                    gid_vc_list = []
                    for index in range(len(gid_list)):
                        gid_vc_atom = []
                        if gid_list[index][1].split()[-1][4:] == key:
                            gid_vc_atom.append(gid_list[index][1].split()[6][4:])   # vsn
                            gid_vc_atom.append(gid_list[index][1].split()[7][5:])   # ctrl
                            ch_id = gid_list[index][2][1].split()[1][3:] + "_" + gid_list[index][1].split()[2][1:-1]
                            gid_vc_atom.append(ch_id)   # channel
                            gid_vc_list.append(gid_vc_atom)
                            #print "\t\t",gid_list[index]
                    # 把一个虚级联组的 vsn 单独取出来存到列表中排序
                    vsn_list = []
                    for index in range(len(gid_vc_list)):
                        vsn_list.append(gid_vc_list[index][0])
                    vsn_list.sort()
                    # 按照排过序的额 vsn 打印 channel_id
                    for index in range(len(vsn_list)):
                        for indexX in range(len(gid_vc_list)):
                            if vsn_list[index] == gid_vc_list[indexX][0]:
                                if index != len(vsn_list)-1:
                                    print gid_vc_list[indexX][2] + ",",
                                elif index == len(vsn_list)-1:
                                    print gid_vc_list[indexX][2] + " ---",
                    # 判断 vsn 是否正常，如果一个虚级联组的最后一个 vsn_id 等于vsn个数减1，那么认为是正常的
                    if int(vsn_list[-1]) == len(vsn_list) - 1:
                        print "vsn 连续 ---",
                    else:
                        print "vsn 不连续 ---",
                    # 判断 ctrl_id 是否正常，如果前序 ctrl_id 为 2，最后一个 ctrl_id 为 3，那么认为是正常的
                    ctrl_flag = True
                    for index in range(len(gid_vc_list)):
                        if gid_vc_list[index][0] == vsn_list[0]:
                            if gid_vc_list[index][1] == "2":
                                pass
                            else:
                                ctrl_flag = False
                        if gid_vc_list[index][0] == vsn_list[-1]:
                            if gid_vc_list[index][1] == "3":
                                pass
                            else:
                                ctrl_flag = False
                    if ctrl_flag == True:
                        print "ctrl_id 字段正常。"
                    else:
                        print "ctrl_id 字段异常。"
        else:
            print "sth is wrong !"

def ts_thick(print_flag=True):
    fn = open(filename_a, 'r')
    ts_set = set()
    for line in fn:
        if "ts:" in line:
            list_tmp = line.split()
            for i in list_tmp:
                if "frame" in i:
                    ts_set.add(i[7:])
    fn.close
    list_type_ts = list(ts_set)
    dict_ts = {}
    for index in range(len(list_type_ts)):
        dict_ts[list_type_ts[index]] = 0
        fn = open(filename_a, 'r')
        for line in fn:
            if "ts" in line and "framer:"+list_type_ts[index] in line:
                dict_ts[list_type_ts[index]] += len(line.split("(")[1].split(")")[0].strip().split())
        fn.close
    if print_flag:
        print "时隙通道中类型信息如下：\n\t",
        for key in dict_ts.keys():
            if key != dict_ts.keys()[-1]:
                print "%s 链路 %d 条；" % (key, dict_ts[key]),
            else:
                print "%s 链路 %d 条。" % (key, dict_ts[key])
    return list_type_ts, dict_ts


def channel_ts(channel_a, type_a):
    if channel_a == "ts":
        print "%s 的通道列表如下：" % type_a
        list_tu1x_info = []
        info_tmp = []
        for index in range(len(line_tu1X)):
            info_tmp.append(line_tu1X[index][0])
            info_tmp.append(line_tu1X[index][2][1].split()[1][3:] + "_" + line_tu1X[index][1].split()[2][1:-1])
            list_tu1x_info.append(info_tmp)
            info_tmp = []
    for index in range(len(list_tu1x_info) - 1):
        line_start = list_tu1x_info[index][0]
        line_end = list_tu1x_info[index+1][0]
        head_print_flag = False
        ts_content_all = []
        for line_num in range(line_start, line_end):
            line_txt = linecache.getline(filename_a, line_num)
            ts_content_tmp = []
            if "ts" in line_txt and "framer:"+type_a in line_txt:
                head_print_flag = True
                ts_content_tmp = line_txt.split("(")[1].split(")")[0].strip().split()
            ts_content_all += ts_content_tmp
        ts_content_all = list(map(int,ts_content_all))
        ts_content_all.sort()
        ts_content_all = list(map(str,ts_content_all))
        if head_print_flag == True:
            print "\t%s：" % list_tu1x_info[index][1],
            print "%s" % ", ".join(ts_content_all)


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvf:a:c:t:", ["help", "version", "filename=", "abstract=", "channel=", "type="])
        if len(opts) == 0:
            usage()
        for name, value in opts:
            if name in ('-h', '--help'):
                usage()
            elif name in ('-v', '--version'):
                version()
            elif name in ('-f', '--filename'):
                filename_a = value
                filename_check(filename_a)
            elif name in ('-a', '--abstract'):
                abstract_a = value
                abstract_check(abstract_a)
            elif name in ('-c', '--channel'):
                channel_a = value
                channel_check(channel_a)
            elif name in ('-t', '--type'):
                type_a = value
                type_check(type_a)
        if abstract_a == "" and channel_a == "" and type_a == "":
            usage()
    except getopt.GetoptError:
        usage()
   

    line_stmX = line_stmX_pop(filename_a)
    stmX_type_set = stmX_type_set_pop(line_stmX)
    line_tugX = line_tugX_pop(filename_a)
    tugX_type_set = tugX_type_set_pop(line_tugX)
    line_tu1X = line_tu1X_pop(filename_a)
    tu1X_type_set = tu1X_type_set_pop(line_tu1X)


    if abstract_a == "stm-x":
        rate_identify(line_stmX)
        print "*" * 80
        stmx_thick(line_stmX, stmX_type_set)
        stmx_thin(line_stmX, stmX_type_set)
        print "*" * 80

    elif abstract_a == "tugx":
        print "*" * 80
        tugx_thick(line_tugX, tugX_type_set)
        print "*" * 80
        
    elif abstract_a == "tu1x":
        print "*" * 80
        tu1x_thick(line_tu1X, tu1X_type_set)
        print "*" * 80
    elif abstract_a == "ts":
        print "*" * 80
        ts_thick()
        print "*" * 80
    else:
        pass
   

    if channel_a[:4] == "stm-" and type_a in ["pos", "atm", "null"]:
        print "*" * 80
        channel_pan(channel_a, type_a)
        print "*" * 80
    if channel_a == "stm-1" and type_a in ["gfp_s", "gfp_v", "gfp"]:
        print "*" * 80
        if type_a in ["gfp_s", "gfp_v"]:
            gfp_check(channel_a, type_a)
        if type_a == "gfp":
            gfp_check(channel_a, "gfp_s")
            gfp_check(channel_a, "gfp_v")
        print "*" * 80
    if channel_a == "tug3" and type_a in ["hdlc", "tug2s", "null"]:
        print "*" * 80
        channel_thn(channel_a, type_a)
        print "*" * 80
    if channel_a == "tug3" and type_a in ["gfp_s", "gfp_v", "gfp"]:
        print "*" * 80
        if type_a in ["gfp_s", "gfp_v"]:
            gfp_tug3_check(channel_a, type_a)
        if type_a == "gfp":
            gfp_tug3_check(channel_a, "gfp_s")
            gfp_tug3_check(channel_a, "gfp_v")
        print "*" * 80
    if channel_a == "tu1x" and type_a in ["hdlc", "E1", "null"]:
        print "*" * 80
        channel_ne1(channel_a, type_a)
        print "*" * 80
    if channel_a == "tu1x" and type_a in ["gfp_s", "gfp_v", "gfp"]:
        print "*" * 80
        if type_a in ["gfp_s", "gfp_v"]:
            gfp_tu1x_check(channel_a, type_a)
        if type_a == "gfp":
            gfp_tu1x_check(channel_a, "gfp_s")
            gfp_tu1x_check(channel_a, "gfp_v")
        print "*" * 80
    if channel_a == "ts":
        print "*" * 80
        channel_ts(channel_a, type_a)
        print "*" * 80




