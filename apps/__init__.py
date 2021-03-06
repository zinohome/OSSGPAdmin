#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAdmin

from flask import Flask
from flask_caching import Cache
from flask_login import LoginManager
from importlib import import_module
from utils.restclient import OSSGPClient
from decouple import config
from utils import log
import flask_monitoringdashboard as dashboard

'''logging'''
log = log.Logger(level=config('OSSGPADMIN_APP_LOG_LEVEL', default='INFO'))

login_manager = LoginManager()

'''cache'''
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

def register_extensions(app):
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home', 'ossgov', 'govass', 'infra', 'sysdev', 'sysadmin', 'jsontool', 'syshelp'):
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
    cache.init_app(app)
    dashboard.bind(app)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app
