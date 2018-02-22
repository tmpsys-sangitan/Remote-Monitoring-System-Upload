#!/bin/sh

# 起動スクリプト
# chmod 755 run.sh で権限を付けてから実行すること

nohup python upload.py upload > /dev/null 2> /dev/null < /dev/null &
