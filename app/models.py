#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db


class Port(db.Model):
    __tablename__ = 'Port'
    id = db.Column(db.Integer, primary_key=True)
    port = db.Column(db.Integer, unique=True, index=True)
    password = db.Column(db.String(10))
    created_date = db.Column(db.DateTime)
    expired_date = db.Column(db.DateTime)
    valid = db.Column(db.Boolean)
    note = db.Column(db.Text)

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
            'created_date': self.created_date.timestamp(),
            'expired_date': self.expired_date.timestamp(),
            'valid': self.valid,
            'note': self.note
        }
