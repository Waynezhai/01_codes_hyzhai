#########################################################################
# File Name: sc_003_snmpExpReplaceT2.sh
# Author: Wayne_zhy
# Mail: zhyzhaihuiyan@163.com
# Created Time: 2019-11-27 11:08:55
# Last modified: 2019-11-27 11:08:55
#########################################################################
#!/bin/bash

mdkir /tmp/snmp_test
cd /tmp/snmp_test

cp /appfs/apps/optiway_expII/optiway_expII_V1.5.686.tar.gz ./
tar -zxvf optiway_expII_V1.5.686.tar.gz 
cd ./addon
tar -jxvf snmp.tar.bz2
cp ./bin/* /usr/local/bin -rf
cp ./etc/* /usr/local/etc -rf

/usr/local/bin/rc.snmp
exit 0

