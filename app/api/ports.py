#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, current_app, session
from datetime import datetime, timedelta
from . import api
from .. import db
from ..models import Port
from ..utils.decorators import admin_required
from ..utils import now, \
    User, \
    server, \
    gen_port_passwords, \
    get_occupied_ports, \
    restart_shadowsocks
from ..utils.scheduler import filter_invalid_ports


@api.route('/test', methods=['GET', 'POST', 'PUT', 'DELETE'])
@admin_required
def test():
    print(type(session), session, dict(session))
    result = filter_invalid_ports()
    return jsonify(result)


@api.route('/ports')
@admin_required
def get_all_ports():
    return jsonify(list(map(lambda config: config.dict(), Port.query.all())))


@api.route('/port', methods=['POST'])
@admin_required
def add_port():
    form = request.form
    created_date = now()

    if form['auto_create']:
        try:
            port, password = gen_port_passwords()
        except StopIteration:
            return jsonify('Max Port!'), 500
    else:
        port, password = (form['port'], form['password'])

    # expired_date 是 port 到期的日期，精确到天数，不是秒
    # 值为 0, 1, 2, 3 可根据自己需求添加做判断
    # 0 是自己选择的日期，所以有额外的字段 expired_date_unix 来保存到期日期的时间戳
    # 1 是 3 天，2 是一个月，3 是1 年
    if form['expired_date'] == '0':
        expired_date = datetime.fromtimestamp(form['expired_date_unix'])
    elif form['expired_date'] == '1':
        expired_date = created_date + timedelta(days=3)
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

    server.add(port, password)
    server.save()

    note = 'Created on {0}, this config will be expired after 30 days on {1}'
    user = User(port, password)
    user.note(note.format(created_date, expired_date))
    user.save()

    db.session.add(new_port)
    db.session.commit()
    return jsonify('Success!')

    # status = restart_shadowsocks()
    # if status is 0:
    #     return jsonify('Success!')
    # else:
    #     return jsonify('Shadowsocks restart error! Please restart manually!'), 500


@api.route('/port', methods=['PUT'])
@admin_required
def update_port():
    form = request.form
    port = Port.query.filter_by(id=int(form['id'])).first_or_404()
    occupied_ports = get_occupied_ports()

    if 'port' in form:
        if form['port'] not in occupied_ports:
            port.port = form['port']
        else:
            return jsonify('Port in use!'), 409

    if 'password' in form:
        port.password = form['password']

    if 'created_date' in form:
        port.created_date = datetime.fromtimestamp(int(float(form['created_date'])))

    if 'expired_date' in form:
        port.expired_date = datetime.fromtimestamp(int(float(form['expired_date'])))

    if 'valid' in form:
        port.valid = True if form['valid'] == 'true' else False

    if 'note' in form:
        port.note = form['note']

    if port.valid:
        if 'port' in form or 'password' in form:
            User(port.port, port.password).save()
            server.update(port.port, port.password)
            server.save()
    else:
        server.delete(port.port)
        server.save()

    db.session.commit()
    return jsonify('Success!')

    # status = restart_shadowsocks()
    # if status is 0:
    #     return jsonify('Success!')
    # else:
    #     return jsonify('Shadowsocks restart error! Please restart manually!'), 500


@api.route('/port', methods=['DELETE'])
@admin_required
def delete_port():
    form = request.form
    port = Port.query.filter_by(id=form['id']).first_or_404()

    User.delete(port.port)
    server.delete(port.port)
    server.save()

    db.session.delete(port)
    db.session.commit()
    return jsonify('Success!')

    # status = restart_shadowsocks()
    # if status is 0:
    #     return jsonify('Success!')
    # else:
    #     return jsonify('Shadowsocks restart error! Please restart manually!'), 500
