#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import login_manager
from settings import USERNAME, PASSWORD, EMAIL


class Permission:
    READ = 1
    ADMINISTER = 2


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    ports = db.relationship('Port', backref='user')

    def __repr__(self):
        return '<User {name}>'.format(name=self.username)

    @staticmethod
    def add_admin():
        print('注册管理员账号中...')
        admin = User(username=USERNAME, password=PASSWORD, email=EMAIL, is_admin=True)
        db.session.add(admin)
        db.session.commit()
        token = admin.generate_confirmation_token()
        admin.confirm(token)
        print('管理员账号注册成功！')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def is_administrator(self):
        return self.is_admin


class AnonymousUser(AnonymousUserMixin):
    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


class Port(db.Model):
    __tablename__ = 'ports'
    id = db.Column(db.Integer, primary_key=True)
    port = db.Column(db.Integer, unique=True, index=True)
    password = db.Column(db.String(10))
    created_date = db.Column(db.DateTime)
    expired_date = db.Column(db.DateTime)
    valid = db.Column(db.Boolean)
    note = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Port No.{id}: {port}>'.format(
            id=self.id,
            port=self.port
        )

    def __getitem__(self, item):
        data = {
            'id': self.id,
            'port': self.port,
            'password': self.password,
            'created_date': self.created_date.timestamp(),
            'expired_date': self.expired_date.timestamp(),
            'valid': self.valid,
            'note': self.note
        }

        return data[item]

    def dict(self):
        return {
            'id': self.id,
            'port': self.port,
            'password': self.password,
            'created_date': int(self.created_date.timestamp()),
            'expired_date': int(self.expired_date.timestamp()),
            'valid': self.valid,
            'note': self.note,
            'file': '/files/config-{port}.json'.format(port=self.port)
        }
