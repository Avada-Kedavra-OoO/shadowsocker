#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from .files_object import server
from .utils import now
from ..models import Port
from .. import db


def filter_invalid_ports():
    """
    过滤掉过期的端口
    :return:
    """
    current_app.logger.info('Start Checking Ports...')
    ports = Port.query.all()
    for port in ports:
        if port.expired_date.timestamp() < now().timestamp() and port.valid:
            server.delete(port.port)
            port.valid = False

    server.save()
    db.session.commit()
    current_app.logger.info('Checking Ports Successfully!')

    return 'Success!'


def auto_check_ports(app):
    """
    建立一个定时任务，周期进行端口检查
    :return:
    """
    with app.app_context():
        return filter_invalid_ports()
