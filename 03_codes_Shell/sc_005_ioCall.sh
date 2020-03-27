#########################################################################
# File Name: sc_005_ioCall.sh
# Author: Wayne_zhy
# mail: zhyzhaihuiyan@163.com
# Created Time: 2020-03-18 17:02:19
# Last Modified: 2020-03-18 17:02:22
#########################################################################
#!/bin/bash

DEBUG=false
declare -i TIMES=10
declare -i SIZE=500

for loop in `seq 1 $TIMES`; do
    rm /tmp/test_${SIZE}M -rf
    mkdir /tmp/test_${SIZE}M
    cd /tmp/test_${SIZE}M
    [ $DEBUG ] && echo "创建/tmp下的测试目录"
    dd if=/dev/zero of=test_${SIZE}M.test bs=1M count=$SIZE 2> /dev/null
    [ $DEBUG ] && echo "创建测试文件 test_${SIZE}M.test"
    cp test_${SIZE}M.test test_${SIZE}M.cp
    [ $DEBUG ] && echo "创建 test_${SIZE}M.test 的副本 test_${SIZE}M.cp"
    tar -zcf test_${SIZE}M.tar.gz test_${SIZE}M.test
    [ $DEBUG ] && echo "压缩测试文件 test_${SIZE}M.test 为 test_${SIZE}M.tar.gz"
    mkdir /tmp/test_${SIZE}M/tar.dir
    tar -zxf test_${SIZE}M.tar.gz -C /tmp/test_${SIZE}M/tar.dir/
    [ $DEBUG ] && echo "解压缩 test_${SIZE}M.tar.gz 到/tmp/test_${SIZE}/tar.dir"
    echo "第 $loop 次测试完成！"
    sync
    echo 1 > /proc/sys/vm/drop_caches
    echo 2 > /proc/sys/vm/drop_caches
    echo 3 > /proc/sys/vm/drop_caches
    sleep 60
done

