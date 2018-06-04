#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
蓝本（Blueprint）是 Flask 用来对路由进行模块化的一个组件

正常情况下，路由只能在 app 初始化后定义，
但现在程序在运行的时候创建，只有在调用 create_app() 之后才能使用 app.route 路由器，
这时定义路由就太晚了。

通过蓝本定义路由，这些路由会处于休眠状态，
直到蓝本注册到 app 上后，路由才会真正成为 app 的一部分。

使用全局作用域的蓝本时，定义路由的方法几乎和单脚本 app 一样。

"""

from flask import Blueprint

main = Blueprint('main', __name__)

# 定义的路由需要在该脚本的末尾导入，避免循环导入依赖
from . import views
