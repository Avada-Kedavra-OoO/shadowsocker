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
