#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAPI

from sys import exit
from decouple import config
from utils import log

from apps.config import config_dict
from apps import create_app

'''logging'''
log = log.Logger(level=config('OSSGPADMIN_APP_LOG_LEVEL', default='INFO'))


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


if DEBUG:
    log.logger.info('DEBUG       = ' + str(DEBUG))
    log.logger.info('Environment = ' + get_config_mode)

if __name__ == "__main__":
    app.run()
