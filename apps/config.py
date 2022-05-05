#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAdmin

import os
from decouple import config
from env.environment import Environment
from utils import log

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPADMIN_APP_LOG_LEVEL'))

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    appdir = os.path.abspath(os.path.join(basedir, os.pardir))
    # Set up the App SECRET_KEY
    SECRET_KEY = config('OSSGPADMIN_APP_SECRET', default='S#perS3crEt_007')
    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

class DebugConfig(Config):
    DEBUG = True
    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
