#!/bin/bash
#filename=link_check_$(date +%Y%m%d%H%M%S).txt
#touch /tmp/$filename
date_day=$(date +%Y%m%d)
mkdir -p /tmp/rate_rec/rate_rec_$date_day
cd /tmp/rate_rec/

while :
do
	if [ "$(($(date +%Y%m%d)-$date_day))" != "0" ];then
		#filename=link_check_$(date +%Y%m%d%H%M%S).txt
		tar -zcvf rate_rec_$date_day.tar.gz ./rate_rec_$date_day  > /dev/null
		rm -rf ./rate_rec_$date_day
		if [ `ls -l ./*.tar.gz |wc -l` == "8" ];then
			rm -rf `ls ./*.tar.gz -lhtv|awk 'NR==1{print }'|awk '{print $9}'`			
		fi
		date_day=$(date +%Y%m%d)
		mkdir -p /tmp/rate_rec/rate_rec_$date_day		
	fi

		date +%Y-%m-%d-%H:%M:%S >aaa.tmp
		/usr/local/bin/cli -c "show interface 1/f/1-13 counter" |grep "Tx Bytes" |awk {'print $5'} >>aaa.tmp
		awk '{if(0 == NR % 14) printf("%s\n", $0); else printf("%s,",$0) }' aaa.tmp >>/tmp/rate_rec/rate_rec_$date_day/01_frongt_if_yd_sAndTdmTx.csv
		
		date +%Y-%m-%d-%H:%M:%S >bbb.tmp
		/usr/local/bin/cli -c "show interface 1/b/21,33 counter" |grep "Tx Pkts" |awk {'print $5'} >>bbb.tmp
		awk '{if(0 == NR % 3) printf("%s\n", $0); else printf("%s,",$0) }' bbb.tmp >>/tmp/rate_rec/rate_rec_$date_day/02_backplane_yd_sTxToX86.csv
		
		date +%Y-%m-%d-%H:%M:%S >ccc.tmp
		/usr/local/bin/cli -c "show interface 1/b/9,17,25 counter" |grep "Rx Pkts" |awk {'print $5'} >>ccc.tmp
		awk '{if(0 == NR % 4) printf("%s\n", $0); else printf("%s,",$0) }' ccc.tmp >>/tmp/rate_rec/rate_rec_$date_day/03_backplane_yd_inCardTx.csv
		
		date +%Y-%m-%d-%H:%M:%S >ddd.tmp
		/usr/local/bin/cli -c "show interface 2/f/1 counter" |grep "Tx Bytes" |awk {'print $5'} >>ddd.tmp
		/usr/local/bin/cli -c "show interface 2/b/29 counter" |grep "Rx Bytes" |awk {'print $5'} >>ddd.tmp
		/usr/local/bin/cli -c "show interface 2/f/2-3,6 counter" |grep "Tx Bytes" |awk {'print $5'} >>ddd.tmp
		awk '{if(0 == NR % 6) printf("%s\n", $0); else printf("%s,",$0) }' ddd.tmp >>/tmp/rate_rec/rate_rec_$date_day/04_frongt_if_lt_sAndTdmTx.csv
		
		date +%Y-%m-%d-%H:%M:%S >eee.tmp
		/usr/local/bin/cli -c "show interface 2/f/1 counter" |grep "Tx Bytes" |awk {'print $5'} >>eee.tmp
		a=`/usr/local/bin/cli -c "show interface 2/f/1 counter" |grep "Tx Bytes" |awk {'print $5'}`
		b=`/usr/local/bin/cli -c "show interface 2/b/29 counter" |grep "Rx Bytes" |awk {'print $5'}`
		echo `expr $a - $b`>>eee.tmp
		/usr/local/bin/cli -c "show interface 2/f/4-5 counter" |grep "Tx Bytes" |awk {'print $5'} >>eee.tmp
    		awk '{if(0 == NR % 5) printf("%s\n", $0); else printf("%s,",$0) }' eee.tmp >>/tmp/rate_rec/rate_rec_$date_day/05_frongt_if_lt_sAndAtmTx.csv
    	sleep 1 
	
done

