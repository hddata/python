#!/bin/bash   

#trust.sh-v1.1

checkfile()
{
  if [ ! -f $1 ]
  then
    echo "[ERROR] $1 is not exist,please check the file!"
    exit 1
  fi  
}
setkey()
{
  num=`sed -n '$=' $1`
  for i in `seq $num`;do
    #ip  user address
    ip=`awk ''NR==$i' {print $1}' $1`
    user=`awk ''NR==$i' {print $2}' $1`
    pass=`awk ''NR==$i' {print $3}' $1`
    echo "------"$ip"------"
    sshpass -p "$pass" ssh -t $user@$ip -o StrictHostKeyChecking=no "rm -rf ~/.ssh;\
    ssh-keygen -t rsa -f ~/.ssh/id_rsa -P ''" &> /dev/null
    if [ $? -eq 0 ] ; then
        echo -e "成功建立公钥和私钥"
    else
        echo "error: " $?
    fi
    
    sshpass -p "$pass" scp -o StrictHostKeyChecking=no $user@$ip:~/.ssh/id_rsa.pub ~/id_rsa.pub1
    
    if [ $? -eq 0 ] ; then
        echo -e "公钥成功传回本地\n"
    else
        echo "error: " $?
    fi
    cat ~/id_rsa.pub1 >> authorized_keys
    rm -rf ~/.ssh/id_rsa.pub1
  done
}

var=`rpm -qa|grep sshpass`
if [ ! -n "$var" ]; then
  echo "you should install sshpass first"
  read -p "是否安装sshpass？是(y)---否(其他): "  tem
  if [ "$tem" == 'y' -o "$tem" == 'Y' ]; then
    rpm -vih sshpass-1.05-7.1.x86_64.rpm
    rpm -ev sshpass-1.05-7.1.x86_64 --nodeps
  else
    exit 0
  fi
fi

file_name1=$1
cwd=$(pwd)
cd $cwd
hostlist_file1="$cwd/$file_name1"
checkfile $hostlist_file1
sed -i '/^ *$/d' $hostlist_file1

if [ "$#" -eq 1 ] ; then
    rm -rf authorized_keysrm
    setkey $hostlist_file1 #互信hostlist_file1里面的主机
elif [ "$#" -eq 2 ] ; then
    file_name2=$2
    hostlist_file2="$cwd/$file_name2"
    checkfile $hostlist_file2
    sed -i '/^ *$/d' $hostlist_file2 
    h2=`sed -n '$=' $hostlist_file2`
    if [ "$h2" -eq 0 ] ; then 
  	    echo $hostlist_file2"错误"
  	    exit 1
    else
  	    while read line
        do
          if cat $hostlist_file1 | grep "$line" >/dev/null ;then
              echo $line"已经在互信的名单里了"
              sed -i "/$line/d" $hostlist_file2
          fi
       done < $hostlist_file2
    fi
   #############
   setkey $hostlist_file2 $cmd_file
   cat $hostlist_file2 >> $hostlist_file1
else
	echo "参数错误"
	exit 1
fi

chmod 600 authorized_keys
num=`sed -n '$=' $hostlist_file1`
for i in `seq $num`;do
    ip=`awk ''NR==$i' {print $1}' $hostlist_file1`
    user=`awk ''NR==$i' {print $2}' $hostlist_file1`
    pass=`awk ''NR==$i' {print $3}' $hostlist_file1`
    sshpass -p "$pass" scp authorized_keys  $user@$ip:~/.ssh/
done
if [ $? -eq 0 ] ; then
   echo -e "公钥成功发送到个主机\n"
else
  echo "error: " $?
fi

num=`sed -n '$=' $hostlist_file1`
for i in `seq $num`;do
  ip1=`awk ''NR==$num' {print $1}' $hostlist_file1`
  user1=`awk ''NR==$num' {print $2}' $hostlist_file1`
  pass1=`awk ''NR==$num' {print $3}' $hostlist_file1`
  echo -e "------------测试------------\n通过" $user1@$ip1 "登陆其他主机"
  for i in `seq $num`;do
    ip=`awk ''NR==$i' {print $1}' $hostlist_file1`
    user=`awk ''NR==$i' {print $2}' $hostlist_file1`
    echo "------"$user"@"$ip"------"
    sshpass -p $pass1 ssh $user1@$ip1 "ssh -oStrictHostKeyChecking=no $user@$ip date 2>/dev/null"
  done
done

if [ $? -eq 0 ] ; then
   echo -e "互信成功\n"
else
  echo "error: " $?
fi
