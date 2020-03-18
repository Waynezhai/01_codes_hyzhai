#!/usr/bin/env python
#-*- coding:utf8 -*-
################################################################# 
# FileName: sonOfString.py
# Author: Wayne_zhy
# Mail: zhyzhaihuiyan@163.com
# Created Time: 2020-03-09 22:10:04
# Last Modified: 2020-03-09 23:07:50
################################################################# 


string = raw_input("请输入一个字符串，区分大小写且长度小于100：")
#string = "abcdab"
string_blank = " ".join(string)
string_list_pre = string_blank.split()

string_list = []
for i in range(len(string_list_pre)):
    if string_list_pre[i] not in string_list:
        string_list.append(string_list_pre[i])

string_index_list = range(len(string_list))

sub_list_all = []
for i in range(1 << len(string_index_list)):
    combo_list = []
    for j in range(len(string_index_list)):
        if i & (1 << j):
            combo_list.append(string_index_list[j])
    sub_list_all.append(combo_list)

sub_list_all.pop(0)
#print len(sub_list_all)
#print sub_list_all
#print "*" * 80
result_list = []
for i in range(len(sub_list_all)):
    single = ""
    for j in range(len(sub_list_all[i])):
        if string[sub_list_all[i][j]] in single:
            continue
        else:
            single = single + string[sub_list_all[i][j]]
    if single not in result_list:
        result_list.append(single)

#print result_list
for i in range(len(result_list)):
    print result_list[i]

