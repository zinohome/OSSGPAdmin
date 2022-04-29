# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask
from flask_login import LoginManager
from importlib import import_module
from utils.restclient import OSSGPClient
from decouple import config
from utils import log

'''logging'''
log = log.Logger(level=config('OSSGPADMIN_APP_LOG_LEVEL', default='INFO'))

oc = OSSGPClient(config('OSSGPADMIN_APP_API_USER', default='admin'), config('OSSGPADMIN_APP_API_PASSWORD', default='passw0rd'))
login_manager = LoginManager()


def register_extensions(app):
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_app():
        pass

    @app.teardown_request
    def shutdown_session(exception=None):
        pass


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app
