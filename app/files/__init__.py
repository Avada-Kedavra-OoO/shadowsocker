#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

file = Blueprint('files', __name__)

from . import files
