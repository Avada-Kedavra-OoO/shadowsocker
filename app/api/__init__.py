#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个包是 Flask 蓝本生成的路由的模块，用来封装后台 API 的接口

蓝本的具体说明参考 main 包下的注释

"""

from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

from . import ports


@api.route('/')
def hello():
    return jsonify('Hello')
