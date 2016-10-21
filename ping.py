# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    @Version:     python-2.7.12
    @FileName：   ping.py
    @Author:      cnshhi
    @CreateTime:  2016/9/23 15:19
    @Email:       cnshi@travelsky.com
    @Description:

time ping www.1.com -c 5
5是发送5个包
"""
import re
import os
import subprocess
import linecache

count = 0
arr = []
f = 'temp.log'
f1 = 'ping_info.log'

for i in xrange(0x0,0xA):
    arr.append(str(i))

for i in xrange(26):
    # arr.append(chr(i+ord('A')))
    arr.append(chr(i + ord('a')))

for i in arr:
    """发5个包，间隔1秒发一次"""
    pin = 'ping ' + 'www.' + i + '.com' ' -c 5 -i 1'
    p = subprocess.Popen(pin, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    a = p.wait()
    ret = p.stdout.read()
    fin = open(f, 'w')
    fin.write(ret)
    fin.close()
    file1 = open(f, 'r')
    line_count = len(file1.readlines())
    file1.close()
    linecache.clearcache()
    a1 = linecache.getline(f, 1)
    ip = str(re.findall("(?<=[(])[^()]+\.[^()]+(?=[)])", a1))[2:-2]
    address = 'www.' + i + '.com'
    a2 = linecache.getline(f, line_count - 1)
    temp = int(re.findall(r'(\w*[0-9]+)\w*', a2)[1])
    if temp == 0:
        status = "----ping failed----"
    else:
        status = "----ping success----"
        count += 1
    info = address + ' ip:' + ip + status
    fin = open(f1, 'aw+')
    fin.write(info)
    fin.write("\n")
    fin.close()
fin = open(f1, 'aw+')
fin.write("成功ping通的ip个数%d" % count)
fin.write("\n")
fin.close()

if os.path.exists(f):
    os.remove(f)
print "finish"



