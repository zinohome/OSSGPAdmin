# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import os

from flask_migrate import Migrate
from sys import exit
from decouple import config
from env.environment import Environment
from utils import log

from apps.config import config_dict
from apps import create_app, db

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPADMIN_APP_LOG_LEVEL'))


# WARNING: Don't run with debug turned on in production!
DEBUG = config('OSSGPADMIN_APP_DEBUG', default=True, cast=bool)
#log.logger.debug(config('OSSGPADMIN_APP_SECRET'))

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
#Migrate(app, db)

if DEBUG:
    log.logger.info('DEBUG       = ' + str(DEBUG))
    log.logger.info('Environment = ' + get_config_mode)
    log.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)

if __name__ == "__main__":
    app.run()
