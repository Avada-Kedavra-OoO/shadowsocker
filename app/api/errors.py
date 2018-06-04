#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from flask import render_template, jsonify, current_app, request
from app.main import main


@main.app_errorhandler(404)
def page_not_found():
    return render_template('index.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return jsonify({
        'status': 500,
        'error': dict(e)
    })


@main.app_errorhandler(Exception)
def api_error_handler(e):
    current_app.logger.error('--------- Error Happened in Error Handler --------')
    current_app.logger.error(e)
    if request.method is not 'GET':
        current_app.logger.error('Request.form: ', request.form)
    current_app.logger.error(traceback.format_exc())
    current_app.logger.error('--------------------------------------------------')
    raise e
