#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
2016-07-21--mysqldump.py-v1.0
"""
import os
from time import *
import sys
import mysql.connector
import subprocess
import shutil

STIME=strftime('%Y-%m-%d', localtime(time()))
STIME1=strftime('%Y-%m-%d_%k:%M:%S', localtime(time()))
BACKUP='/backup/'
BACKUP_PATH=BACKUP+'/backup_file/'
MYSQL_BIN_PATH='/usr/bin/'
mycnf="[mysqldump]\nuser=root\npassword=123456\n"
my=r'/etc/my.cnf'
my1=r'/etc/my1.cnf'

shutil.copy(my,my1)
file=open(my,'w')
file.write(mycnf)
file.close()

if not os.path.exists(BACKUP):
    os.mkdir(BACKUP)
if not os.path.exists(BACKUP_PATH):
    os.mkdir(BACKUP_PATH)
#
config = {'host': '127.0.0.1',
          'user': 'root',
          'password': '123456',
          'port': 3306,
          'database': 'mysql',
          'charset': 'utf8',
          'unix_socket': '/var/lib/mysql/mysql.sock'
          }
try:
  conn=mysql.connector.connect(**config)
except mysql.connector.Error as e:
  print('connect fails!{}'.format(e))
cursor = conn.cursor()
sql_show_databases= 'show databases; '
cursor.execute(sql_show_databases)
result_set = cursor.fetchall()
a=str(u' '.join([v[0] for v in result_set]))
databases=a.split(" ")
if "performance_schema" in databases:
    databases.remove("performance_schema")
if "information_schema" in databases:
    databases.remove("information_schema")
cursor.close()
conn.close()
#
f=BACKUP_PATH+'backup.log'
fin = open(f, 'aw+')
for dbname in databases:
    print >>fin,"%s start backup database %s"%(STIME1,dbname)
    os.chdir(MYSQL_BIN_PATH)
    mysqldump = "mysqldump --opt --compress %s" % (dbname)
    f1 = BACKUP_PATH + "backup-%s-%s.sql" % (dbname, STIME)
    child1 = subprocess.Popen(mysqldump, stdout=subprocess.PIPE, shell=True)
    temp = child1.stdout.read()
    fin1 = open(f1, 'w')
    try:
        fin1.write(temp)
        print >> fin, "%s end backup database %s" % (STIME1, dbname)
    except:
        print >> fin, "%s error backup database %s" % (STIME1, dbname)
    fin1.close()
print  "finish"
fin.close()
if os.path.exists(my):
  os.remove(my)
shutil.copy(my1,my)
if os.path.exists(my1):
  os.remove(my1)