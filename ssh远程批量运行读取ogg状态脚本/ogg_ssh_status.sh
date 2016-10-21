#!/bin/bash   
#ogg_ssh_status.sh-v1.0
#
#$#脚本参数
if [ "$#" -ne 2 ] ; then
    echo "USAGE: $0 -f server_list_file cmd"
    exit -1
fi

file_name=$1
cmd_str=$2
cwd=$(pwd)
cd $cwd
hostlist_file="$cwd/$file_name"
cmd_file="$cwd/$cmd_str"


if [ ! -e $hostlist_file ] ; then
    echo 'hostlist file not exist';
    exit 0
fi

if [ ! -e $cmd_file ] ; then
    echo 'cmd_file file not exist';
    exit 0
fi

var=`rpm -qa|grep sshpass`
if [ ! -n "$var" ]; then
  echo "you should install sshpass first"
  read -p "是否安装sshpass？是(y)---否(其他): "  tem
  if [ "$tem" == 'y' -o "$tem" == 'Y' ]; then
    rpm -vih sshpass-1.05-7.1.x86_64.rpm
  else
    exit 0
  fi
fi


num=`sed -n '$=' $hostlist_file`
for i in `seq $num`;do
    #ip  user address
    ip=`awk ''NR==$i' {print $1}' $hostlist_file`
    user=`awk ''NR==$i' {print $2}' $hostlist_file`
    pass=`awk ''NR==$i' {print $3}' $hostlist_file`
    address=`awk ''NR==$i' {print $4}' $hostlist_file`
    sed -i "2i OGG_HOME=$address" $cmd_file
    echo "------"$ip"------"
    sshpass -p "$pass" ssh -t $user@$ip<$cmd_file
   # ssh $user@$ip "bash"<$cmd_file >ogg.log

    if [ $? -eq 0 ] ; then
        echo "$cmd_str Executed Successfully!"
        echo ""
    else
        echo "error: " $?
    fi

    sed -i '2d' $cmd_file
done
