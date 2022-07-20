#! /bin/bash

echo $PWD
echo $0
DIR=$(dirname $(readlink -f "$0"))
echo $DIR
rm $DIR/app.log
touch $DIR/app.log
nohup python $DIR/main.py > $DIR/app.log 2>&1 
