#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
2016-07-18--ogg_status.py-v1.0 读取ogg状态脚本
2016-07-19--ogg_status.py-v1.1 增加手动输入安装路径
2016-09-08--ogg_status.py-v1.2 整理
"""
import os
import subprocess
import linecache
from time import *
import shutil

Dtime = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
path1 = 'status/'
path=raw_input('Please enter the installation path:')


if os.path.exists(path):
    print " "
else:
    print ("No such directory: %s"%(path))
    path = '/u01/app/ogg/'
    print ("The default installation directory:%s"%(path))
    print " "

path3 = path + path1
if os.path.exists(path3):
    pass
else:
    os.makedirs(path3)

os.chdir(path)
f = path3+'infoall.txt'
fin = open(f,'w')
fin.write('info all')
fin.close()


child1 = subprocess.Popen(["cat",f], stdout=subprocess.PIPE)
child2 = subprocess.Popen(['./ggsci'],stdin=child1.stdout,stdout=subprocess.PIPE,shell=True)
a = child2.wait()
name = child2.stdout.read()
name1 = name.split("MANAGER     RUNNING")[1]
name2 = name1.strip()
name3 = name2.split("\n\n")[0]
name4 = name3.split()
list1 = []
lenth = len(name4)

for i in range(lenth):
  if i%5 == 1 or i%5 == 2:
    list1.append(name4[i])
#####
f7 = path3+'ogg_status.log'
fin = open(f7,'aw+')
fin.write(Dtime)
fin.write("\n")
fin.close()


lenth1 = len(list1)
os.chdir(path)
for i in range(lenth1):
    if i % 2 == 1:
        f5 = path3+'temp.txt'
        fin = open(f5, 'w+')
        fin.write('info ')
        fin.write(list1[i])
        fin.close()
#
        child4 = subprocess.Popen(["cat",f5], stdout=subprocess.PIPE)
        child5 = subprocess.Popen(['./ggsci'], stdin=child4.stdout, stdout=subprocess.PIPE, shell=True)
        a = child5.wait()
        time = child5.stdout.read()
        f6 = path3+'time.txt'
        fin = open(f6,'w')
        fin.write(time)
        fin.close()
#
        file1 = open(f6,'r')
        linecount = len(file1.readlines())
        linecache.clearcache()
        lie3 = []
        lie4 = []
        lie3 = linecache.getline(f6,linecount-3)
        lie4 = lie3[21:40]
#
        fin = open(f7,'aw+')
        fin.write(list1[i-1])
        fin.write(" ")
        fin.write(list1[i])
        fin.write(" ")
        fin.write(lie4)
        fin.write("\n")
        fin.close()
#
fin = open(f7, 'aw+')
fin.write("\n\n")
fin.close()

f8 = path3+'copy_ogg_status.log'
shutil.copy(f7,f8)
fin = open(f8, 'r')
info = fin.read()
fin.close()

print "Status    Group      Time"
print info

if os.path.exists(f):
  os.remove(f)

if os.path.exists(f5):
  os.remove(f5)

if os.path.exists(f6):
  os.remove(f6)

if os.path.exists(f8):
  os.remove(f8)