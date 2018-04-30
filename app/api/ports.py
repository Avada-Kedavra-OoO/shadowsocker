#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request
from datetime import datetime, timedelta, timezone
from settings import TIMEZONE
from . import api
from .. import db
from ..models import Port
from ..utils import \
    User, \
    server, \
    gen_port_passwords, \
    get_occupied_ports


g = gen_port_passwords()


@api.route('/ports')
def get_all_ports():
    return jsonify(list(map(lambda config: config.dict(), Port.query.all())))


@api.route('/port', methods=['POST'])
def add_port():
    form = request.form
    utc_date = datetime.utcnow().replace(tzinfo=timezone.utc)
    created_date = utc_date.astimezone(timezone(timedelta(hours=TIMEZONE)))

    if form['auto_create']:
        try:
            port, password = next(g)
        except StopIteration:
            return jsonify('Max Port!'), 500
    else:
        port, password = (form['port'], form['password'])

    # expired_date 是 port 到期的日期，精确到天数，不是秒
    # 值为 0, 1, 2, 3 可根据自己需求添加做判断
    # 0 是自己选择的日期，所以有额外的字段 expired_date_unix 来保存到期日期的时间戳
    # 1 是 1 天，2 是一个月，3 是1 年
    if form['expired_date'] == '0':
        expired_date = datetime.fromtimestamp(form['expired_date_unix'])
    elif form['expired_date'] == '1':
        expired_date = created_date + timedelta(days=1)
    elif form['expired_date'] == '2':
        expired_date = datetime(created_date.year, created_date.month + 1, created_date.day)
    elif form['expired_date'] == '3':
        expired_date = datetime(created_date.year + 1, created_date.month, created_date.day)
    else:
        expired_date = created_date

    valid = True if expired_date.timestamp() > created_date.timestamp() else False
    new_port = Port(
        port=port,
        password=password,
        created_date=created_date,
        expired_date=expired_date,
        valid=valid,
        note=form['note']
    )

    db.session.add(new_port)
    db.session.commit()
    server.add(port, password)

    note = 'Created on {0}, this config will be expired after 30 days on {1}'
    user = User(port, password)
    user.note(note.format(created_date, expired_date))
    user.save()
    server.save()

    return jsonify('Success!')


@api.route('/port', methods=['PUT'])
def update_port():
    form = request.form
    port = Port.query.filter_by(id=form['id']).first_or_404()
    occupied_ports = get_occupied_ports()

    if 'port' in form and form['port'] not in occupied_ports:
        port.port = form['port']

    if 'password' in form:
        port.password = form['password']

    if 'created_date' in form:
        port.created_date = datetime.fromtimestamp(form['created_date'])

    if 'expired_date' in form:
        port.expired_date = datetime.fromtimestamp(form['expired_date'])

    if 'valid' in form:
        port.valid = form['valid']

    if 'note' in form:
        port.note = form['note']

    db.session.commit()
    return jsonify('Success!')


@api.route('/port', methods=['DELETE'])
def delete_port():
    form = request.form
    port = Port.query.filter_by(id=form['id']).first_or_404()
    db.session.delete(port)
    db.session.commit()
    return jsonify('Success')
