#########################################################################
# File Name: sc_002_remoteReboot.sh
# Author: Wayne_zhy
# mail: zhyzhaihuiyan@163.com
# Created Time: 2020-03-17 14:59:26
# Last Modified: 2020-03-18 16:08:31
#########################################################################
#!/bin/bash

USER=root
IP=10.17.15.153
PWD=123456
declare -i RETIMES=100

auto_reboot_ssh()
{
    expect << EOF
    set timeout 1
    spawn -noecho ssh $USER@$IP "reboot" 
    expect {
        "yes/no" {send "yes\r"; exp_continue}
        "assword" {send "$PWD\r"; exp_continue}
        eof
    }
    catch wait result;
    exit [lindex $result 100]
EOF
}

for loop in `seq 1 $RETIMES` ; do
    ACFLAG=true
    while $ACFLAG; do
        ping -c 5 $IP >> /dev/null
        [ $? -eq 0 ] && ACFLAG=false
        sleep 10
    done
    echo -e "`date`\t\c"
    auto_reboot_ssh >> /dev/null
    [ $? -eq 100 ] && echo "第 ${loop} 次重启成功！" || echo "第 ${loop} 次重启失败！"
    sleep 120
done
