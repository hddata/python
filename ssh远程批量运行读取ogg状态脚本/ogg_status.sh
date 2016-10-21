#! /bin/bash

OGG_status="$OGG_HOME/status"
mkdir -p $OGG_status
echo "info all">$OGG_status/info.txt

cd $OGG_HOME
./ggsci<$OGG_status/info.txt>$OGG_status/status1.txt
sed -n '/Status/,$p' $OGG_status/status1.txt>$OGG_status/status12.txt
sed  -i '/^$/d' $OGG_status/status12.txt
sed -i '1,2d' $OGG_status/status12.txt
sed -i '$d' $OGG_status/status12.txt
awk '{print $2,$3"\n"}' $OGG_status/status12.txt >$OGG_status/status13.txt
sed  -i '/^$/d' $OGG_status/status13.txt
num=`sed -n '$=' $OGG_status/status13.txt`

if [ $num -eq 0 ];then
    echo "no group"
else
    for i in `seq $num`;do
        awk ''NR==$i' {print $2}' $OGG_status/status13.txt>$OGG_status/temp.txt 
        j=`cat $OGG_status/temp.txt | sed 's/^[[:space:]]*//'` 
        echo "info $j">$OGG_status/info.txt 
        ./ggsci<$OGG_status/info.txt>$OGG_status/status2.txt  
        grep -A 5 'Checkpoint Lag' $OGG_status/status2.txt>$OGG_status/status21.txt
        sed -n '3,3p' $OGG_status/status21.txt>$OGG_status/temp.txt  
        awk '{print $1,$2"\n"}' $OGG_status/temp.txt >$OGG_status/status14.txt
        cat $OGG_status/status14.txt | sed -e '/^$/d'>$OGG_status/temp.txt
        cat $OGG_status/temp.txt|cut -c 1-19 >$OGG_status/status14.txt
#
        awk ''NR==$i' {print $1,$2}' $OGG_status/status13.txt>$OGG_status/tem.txt 
        cat $OGG_status/status14.txt>>$OGG_status/tem.txt
        sed ':a ; N;s/\n/ / ; t a ; ' $OGG_status/tem.txt>$OGG_status/status.txt
#
        cat $OGG_status/status.txt>>$OGG_status/wancheng.txt
    done
fi

nowtime=`date +"%Y-%m-%d %H:%M:%S"`
echo "present time "
echo $nowtime
echo "Status  Name  Time    "
cat $OGG_status/wancheng.txt
#echo " "
rm -rf $OGG_status
