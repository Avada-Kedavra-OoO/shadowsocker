#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))

"""
    服务器相关设置
"""
# 服务器的 IP 地址
IP = '127.0.0.1'

# 管理员的初始账号密码
USERNAME = 'admin'
PASSWORD = '123456789'
EMAIL = 'youremail@example.com'

# 服务器分配端口的起始值
START_PORT = 10000

# 服务器分配端口的结束值，注意不包括这个值
# 即服务器不会使用这个端口
END_PORT = 65535

# 服务器要忽略的端口，这些端口在服务器自动生成配置的时候不会使用
# 要指定忽略一定范围的端口，可放置一个长度为2 的二维数组，分别表示端口的起始值和结束值
IGNORE_PORTS = [80, 443, 8080, [10000, 10010]]

# 服务器所在的时区，显示返回时间相关的数据时以该时区为例
# 默认为东8 区
TIMEZONE = 8

"""
    Email 设置
"""
MAIL_SERVER = ''
MAIL_PORT = 587
MAIL_USE_TLS = True

"""
    Shadowsocks 文件设置
"""
# 服务端的 Shadowsocks 配置文件的路径
# 该路径是相对于本配置文件的路径，下同
SHADOWSCOCKS_CONFIG_PATH = os.path.abspath(os.path.join(basedir, 'shadowsocks.json'))

# 服务器生成的用户配置文件的文件夹的路径
USER_CONFIGS_DIRECTORY_PATH = os.path.abspath(os.path.join(basedir, 'output'))

# Shadowsocks 重启命令
SHADOWSCOCKS_RESTART = 'ssserver -c /etc/shadowsocks.json -d start'
