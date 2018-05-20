#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import settings

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, static_folder="./dist/static", template_folder="./dist")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    handler = logging.FileHandler('flask.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
