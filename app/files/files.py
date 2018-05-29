#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import request, send_from_directory, abort
from settings import USER_CONFIGS_DIRECTORY_PATH
from . import file


@file.route('/<filename>')
def download(filename):
    print(os.path.join(USER_CONFIGS_DIRECTORY_PATH, filename))
    if request.method == 'GET':
        if os.path.isfile(os.path.join(USER_CONFIGS_DIRECTORY_PATH, filename)):
            return send_from_directory(USER_CONFIGS_DIRECTORY_PATH, filename, as_attachment=True)
        abort(404)
