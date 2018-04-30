#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import json
import collections
from settings import \
    SHADOWSCOCKS_CONFIG_PATH, \
    USER_CONFIGS_DIRECTORY_PATH, \
    START_PORT, \
    END_PORT, \
    IGNORE_PORTS, \
    IP


class Server(object):
    """
    用来操作服务端 Shadowsocks 配置文件的类

    """

    def __init__(self):
        # 读取服务器配置文件
        with open(SHADOWSCOCKS_CONFIG_PATH, 'r') as f:
            self.conf = json.load(f)
            self.ports = list(
                map(lambda port: int(port), self.conf['port_password'].keys()))
            self.passwords = collections.OrderedDict(
                sorted(self.conf['port_password'].items(), key=lambda t: t[0]))

    def add(self, port, password):
        if port not in self.ports:
            self.passwords[str(port)] = password
            self.ports.append(port)

    def update(self, port, password):
        if port in self.ports:
            self.passwords[str(port)] = password

    def delete(self, port):
        del self.passwords[str(port)]

    def save(self):
        self.conf['port_password'] = self.passwords
        with open(SHADOWSCOCKS_CONFIG_PATH, 'w') as f:
            f.write(json.dumps(self.conf, indent=4))


class User(object):
    """
    用来生成用户配置文件的类

    """
    basic = {
        'configs': [],
        'strategy': None,
        'index': 0,
        'global': False,
        'enabled': True,
        'shareOverLan': False,
        'isDefault': False,
        'localPort': 1080,
        'pacUrl': None,
        'useOnlinePac': False,
        'availabilityStatistics': False,
        'autoCheckUpdate': True,
        'isVerboseLogging': False,
        'logViewer': None,
        'useProxy': False,
        'proxyServer': None,
        'proxyPort': 0
    }

    def __init__(self, port, password):
        self.port = port
        self.data = {
            'auth': False,
            'server': IP,
            'server_port': port,
            'password': password,
            'method': 'aes-256-cfb',
            'remarks': ''
        }

    def note(self, value):
        self.data['note'] = value

    def save(self):
        self.basic['configs'] = [self.data]
        with open(
            '{output}/config-{port}.json'.format(
                output=USER_CONFIGS_DIRECTORY_PATH,
                port=self.port), 'w') as f:
            f.write(json.dumps(self.basic, indent=4))


def get_ignore_ports(ports):
    p = []
    for i in ports:
        if isinstance(i, list):
            for port in range(i[0], i[1]):
                p.append(port)
        else:
            p.append(i)
    return p


server = Server()


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

    :param ports:    已占用的端口的 list
    :return:
    """
    for port in range(max(START_PORT, 0), min(END_PORT, 65535)):
        if port not in set(get_ignore_ports(IGNORE_PORTS) + server.ports):
            password = gen_random_string()
            yield (port, password)

    return None


