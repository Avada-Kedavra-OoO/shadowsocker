#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import api
from .. import db
from ..models import User
from ..email import send_mail
from settings import USERNAME, PASSWORD


@api.route('/login', methods=['POST'])
def login():
    form = request.form
    if form['username'] == USERNAME and form['password'] == PASSWORD:
        login_user()
        return jsonify('Authenticated')
    else:
        return jsonify('Unauthenticated'), 401


@api.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify('Log out')


@api.route('register', methods=['POST'])
def register():
    form = request.form
    user = User(email=form['email'], username=form['username'], password=form['password'])
    db.session.add(user)
    db.session.commit()
    token = user.generate_confirmation_token()
    send_mail(user.email, '确认用户', 'templates/email/confirm', user=user, token=token)
    return jsonify('Temporary Success')


@api.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email, '确认用户', 'templates/email/confirm', user=current_user, token=token)
    return jsonify('Temporary Success')


@api.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return jsonify('Authenticated')

    if current_user.confirm(token):
        return jsonify('Confirmed')
    else:
        return jsonify('Invalid or Expired'), 401


@api.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed:
        return redirect(url_for('api.unconfirmed'))


@api.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return jsonify('Authenticated')
    else:
        return jsonify('Unconfirmed')
