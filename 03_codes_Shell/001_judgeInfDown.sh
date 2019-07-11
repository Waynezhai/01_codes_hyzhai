#########################################################################
# File Name: 001_judgeInfDown.sh
# Author: Wayne_zhy
# mail: zhyzhaihuiyan@163.com
# Created Time: 2019-07-11 15:42:47
# Last Modified: 2019-07-11 15:47:13
#########################################################################
#!/bin/bash

#
# 用这个脚本可以判断恒为分流器设备的端口是否为down，如果down掉就记录down掉时间，并把status的连续三次打印放到记录文件中去
# 根据这个脚本可以很容易地更改出记录进程是否丢失或其他类似的需求
# 这个脚本中有创建以时间命名文件的方法，可以做参考
#


filename=link_check_$(date +%Y%m%d%H%M%S).txt
date_day=$(date +%Y%m%d)
touch /tmp/$filename
for ((i=1;i<=20000000;i=i+1))
do
    sleep 5
    if [ "$(($(date +%Y%m%d)-$date_day))" != "0" ];then
        filename=link_check_$(date +%Y%m%d%H%M%S).txt
        date_day=$(date +%Y%m%d)
    fi
    /usr/local/bin/cli -c "show interface 4,8,12/f/1-2 status" |grep "DOWN">>/dev/null && result=0 || result=1
    if [ "$result" == "0" ];then
        date >> /tmp/$filename 
        echo "======================================================================================">>/tmp/$filename 
        /usr/local/bin/cli -c "show interface 4,8,12/f/1-2 status" >>/tmp/$filename 
        echo "--------------------------------------------------------------------------------------">>/tmp/$filename 
        /usr/local/bin/cli -c "show interface 4,8,12/f/1-2 status" >>/tmp/$filename 
        echo "--------------------------------------------------------------------------------------">>/tmp/$filename 
        /usr/local/bin/cli -c "show interface 4,8,12/f/1-2 status" >>/tmp/$filename 
        echo "--------------------------------------------------------------------------------------">>/tmp/$filename 
    fi
done



