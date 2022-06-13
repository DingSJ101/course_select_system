#! /bin/bash
rm /root/workspace/css/app.log
touch /root/workspace/css/app.log
nohup python /root/workspace/css/main.py > /root/workspace/css/app.log 2>&1 & 
