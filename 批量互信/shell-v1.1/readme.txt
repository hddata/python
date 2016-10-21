hostlist文件格式：ip+空格+user+空格+passwd
hostlist1是第一次互信的文件，之后添加的主机放在hostlist2里
执行语句：sh trust.sh hostlist1
需要添加主机的时候新建文件hostlist2， hostlist2格式和hostlist1一样
执行格式 sh trust.sh hostlist1 hostlist2

trust.sh hostlist1 hostlist2 文件必须在同一路径下 
.sh文件执行之前需要  chmod 755 **.sh