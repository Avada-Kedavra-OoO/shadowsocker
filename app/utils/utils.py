#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from flask import current_app
from subprocess import call
from datetime import datetime, timedelta, timezone
from settings import \
    START_PORT, \
    END_PORT, \
    IGNORE_PORTS, \
    SHADOWSCOCKS_RESTART, \
    TIMEZONE
from .files_object import server


def now():
    utc_date = datetime.utcnow().replace(tzinfo=timezone.utc)
    return utc_date.astimezone(timezone(timedelta(hours=TIMEZONE)))


def get_occupied_ports():
    """
    获取被占用的端口

    :return: 已占用的端口的集合
    """
    p = []
    for i in IGNORE_PORTS:
        if isinstance(i, list):
            for port in range(i[0], i[1]):
                p.append(port)
        else:
            p.append(i)
    return set(p + server.ports)


def gen_random_string(length=10):
    """
    生成随机密码

    :param length:   密码长度，默认为 10 位
    :return:                返回新的密码
    """
    return ''.join(
        random.sample('abcdefghijklmnopqrstuvwxyz1234567890',
                      length))


def gen_port_passwords():
    """
    生成端口和密码对，以元组形式返回

    :return:    端口和密码的集合 (port, password)
    """
    for port in range(max(START_PORT, 0), min(END_PORT, 65535)):
        if port not in get_occupied_ports():
            password = gen_random_string()
            return port, password

    raise StopIteration


def restart_shadowsocks():
    """
    重启 Shadowsocks

    :return:
    """
    current_app.logger.info('Restart Shadowsocks...')
    result = call(SHADOWSCOCKS_RESTART.split(' '))
    current_app.logger.info('Restart Status: {0}'.format(result))

    return result
