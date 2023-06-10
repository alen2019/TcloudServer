import os
import re
import time
import json
import hmac
import base64
import socket
import datetime
import subprocess
import requests
import urllib.parse

def get_ip():
    """
    获取当前服务器ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip =s.getsockname()[0]
    finally:
        s.close()

    return ip

def get_time():
    """
    获取当前时间
    """
    nowTime = datetime.datetime.now()
    return nowTime

def get_number():
    """
    通过当前时间生成一个唯一标签
    """
    nowTime = time.time()
    w = str(nowTime)
    w = w.split('.')[0]
    return w

def port_datection(port):
    """
    检测端口并释放
    """
    commd1 = 'lsof -i:' + str(port)
    network = os.popen(commd1)
    hel = network.readlines()
    for i in hel:
        if 'LISTEN' in i:
            indexstart = i.index('node')+4
            indexend = i.index('root')
            pid = i[indexstart:indexend]
            commd2 = 'kill -9' + str(pid)
            subprocess.Popen(commd2, shell=True)

def appiumStart(port):
    """
    后台启动appium服务（需要把路径改成变量）
    """
    port_datection(port)
    try:
        stdout = open('lsubprocess_stdout','wb')
        stderr = open('/User/alen/subprocess_stdrr','wb')
        cmd = ['/usr/local/bin/appium']
        subprocess.Popen(cmd, stdout=stdout.fileno(),stderr=stderr.fileno())
        return True
    except Exception as e:
        print('启动appiumServer 失败：' + str(e))
        return False


if __name__=='__main__':
    w = get_ip()
    print(w)