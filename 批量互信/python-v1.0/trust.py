# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @Version:     python-2.7.11
    @FileName：   trust.py-v1.0
    @Author:      cnshhi
    @CreateTime:  2016/10/13 9:55
    @Email:       cnshi@travelsky.com
    @Description:
    批量主机互信
    hostlist1是第一次互信的文件，hostlist2是新加的时候的文件
    当hostlist2里有内容的时候互信hostlist2里的，没有的时候互信hostlist1
    互信hostlist2里的时候需要检测里面的主机是否在hostlist1里，没有在的，
    才进行增加的互信

"""
import re
import os
import subprocess

#os.getcwd() 显示当前路径
#os.chdir("/dev") 转换路径
pwd = os.getcwd()
host_file = pwd + '/hostlist1'
host_file1 = pwd + '/host_file1'
host_file2 = pwd + '/hostlist2'
host_file3 = pwd + '/host_file2'
authorized_keys =  pwd + '/authorized_keys'
sshpass = 'sshpass-1.05-7.1.x86_64.rpm'
sshpass_ = pwd + '/' + sshpass


def setup_sshpass(name_):
    temp = name_.split("-")[0]
    name = "rpm -qa|grep %s" % temp
    setup = "rpm -vih %s 2>/dev/null" % name_
    p = subprocess.Popen(name, stdout=subprocess.PIPE, shell=True)
    a = p.wait()
    out = p.stdout.read()
    if temp not in out:
        if os.path.exists(sshpass_):
            p = subprocess.Popen(setup, stdout=subprocess.PIPE, shell=True)
            a = p.wait()
            print "%s  install success" % temp
        else:
            print "%s is not exist,please check the file!" % sshpass_
            exit()
    else:
        print "%s already installed" % temp


def del_blankline(infile, outfile):
    """删除文件空行"""
    infp = open(infile, "r")
    outfp = open(outfile, "w")
    lines = infp.readlines()
    for li in lines:
        if li.split():
            outfp.writelines(li)
            infp.close()
    outfp.close()


def trust(name):
    l = []
    for line in open(name, "r"):
        l = line.split()
        """创建密钥"""
        ip = l[0]
        user = l[1]
        passwd = l[2]
        sshkey1 = 'sshpass -p "' + passwd + '" ssh -t ' + user + '@' + ip + ' -o StrictHostKeyChecking=no '
        sshkey2 = '"rm -rf ~/.ssh;' + 'ssh-keygen -t rsa -f ~/.ssh/id_rsa -P ' + "''" + ' &> /dev/null"'
        sshkey = sshkey1 + sshkey2 + ' 1> /dev/null'
        print "------%s------" % ip
        p = subprocess.Popen(sshkey, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        a = p.wait()
        temp = p.stderr.read()
        if ip not in temp:
            print "[ERROR] 建立公钥和私钥失败"
            exit()
        else:
            print "成功建立公钥和私钥"

        """传回密钥"""
        sshscp = 'sshpass -p "' + passwd + '" scp' + ' -o StrictHostKeyChecking=no ' \
                 + user + '@' + ip + ':~/.ssh/id_rsa.pub ' + pwd + '/id_rsa.pub1'
        p = subprocess.Popen(sshscp, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        a = p.wait()
        temp = p.stderr.read()
        if temp.strip() == '':
            print "公钥成功传回本地"
        else:
            print "[ERROR] 公钥传回失败"
            exit()

        fout = open(authorized_keys, 'aw+')
        fin = open(pwd + '/id_rsa.pub1', 'r')
        line = fin.readlines()
        for eachline in line:
            fout.write(eachline)
        fin.close()
        fout.close()

    if os.path.exists(pwd + '/id_rsa.pub1'):
        os.remove(pwd + '/id_rsa.pub1')
    a = os.system("chmod 600 %s" % authorized_keys)


def send():
    """发送密钥"""
    l = []
    for line in open(host_file, "r"):
        l = line.split()
        ip = l[0]
        user = l[1]
        passwd = l[2]
        sshscp1 = 'sshpass -p "' + passwd + '" scp ' + authorized_keys + ' ' + user + '@' + ip + ':~/.ssh/'
        p = subprocess.Popen(sshscp1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        a = p.wait()
        temp = p.stderr.read()
        if temp.strip() == '':
            print "公钥成功发送到个%s"% ip
        else:
            print "[ERROR] 公钥发送到%s失败" % ip
            exit()

setup_sshpass(sshpass)
"""删除文件1里的空行，并重命名文件1"""
if not os.path.exists(host_file):
    print "%s is not exist,please check the file!" % host_file
    exit()
del_blankline(host_file,host_file1)
if os.path.exists(host_file):
    os.remove(host_file)
os.rename(host_file1,host_file)

if not os.path.exists(host_file2):
    """文件2不存在，互信文件1"""
    if not os.path.exists(authorized_keys):
        f = file(authorized_keys, "w")
        f.close()
    else:
        f = file(authorized_keys, "w")
        f.truncate()
        f.close()
    trust(host_file)
else:
    del_blankline(host_file2, host_file3)
    f = open(host_file2,"w")
    f.truncate()
    f.close()

    data = open(host_file3).read()
    leng = len(data)
    if leng == 0:
        """文件2为空，互信文件1"""
        if not os.path.exists(authorized_keys):
            f = file(authorized_keys, "w")
            f.close()
        else:
            f = file(authorized_keys, "w")
            f.truncate()
            f.close()
        trust(host_file)
    else:
        """文件2不为空，除去原始文件里已经互信的主机"""
        """没有互信的主机写进host_file2"""
        infp = open(host_file3, "r")
        fp = open(host_file, "r")
        outfp = open(host_file2, "w")
        line = infp.readlines()
        lines = fp.readlines()
        for li in line:
            if li in lines:
                print "%s已经在互信名单里了" % li
            else:
                outfp.write(li)
        outfp.close()
        fp.close()
        infp.close()

        data = open(host_file2).read()
        leng = len(data)
        if leng == 0:
            print "新加主机全部已经互信"
            exit()
        else:
            trust(host_file2)
            infp = open(host_file2, "r+")
            outfp = open(host_file, "aw+")
            outfp.write(infp.read())
            outfp.close()
            infp.truncate()
            infp.close()
        """把新加的主机放进文件"""
send()

"""验证"""
print "\n------------测试------------\n"
l = []
l_ = []

for line in open(host_file, "r"):
    l = line.split()
    ip = l[0]
    user = l[1]
    passwd = l[2]
    print "通过%s@%s登陆其他主机" % (user,ip)
    for line1 in open(host_file, "r"):
        l_ = line1.split()
        ip1 = l_[0]
        user1 = l_[1]
        ssh1 = 'sshpass -p "' + passwd + '" ssh ' + user + '@' + ip
        ssh = ssh1 + ' "ssh -oStrictHostKeyChecking=no ' + user1 + '@' + ip1 + ' date 2>/dev/null"'
        p = subprocess.Popen(ssh, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        a = p.wait()
        time = p.stdout.read()
        print "------%s@%s------" % (user1, ip1)
        temp = p.stderr.read()
        if temp.strip() == '':
            print time.replace("\n", "")
        else:
            print "[ERROR] 测试失败"
            exit()
    print " "
f = open(host_file2, "w")
f.truncate()
f.close()
if os.path.exists(host_file1):
    os.remove(host_file1)
if os.path.exists(host_file3):
    os.remove(host_file3)