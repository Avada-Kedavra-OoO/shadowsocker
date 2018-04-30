#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')
