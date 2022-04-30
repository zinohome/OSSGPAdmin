#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAdmin

from apps.sysadmin import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps import log, oc
import time
from decouple import config

@blueprint.route('/sysadmin.html', methods = ['GET', 'POST'])
@login_required
def route_sysadmin():
    today = time.strftime("%Y-%m-%d", time.localtime())
    return render_template('sysadmin/sysadmin.html', segment='sysadmin',
                           startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                           today=today)

@blueprint.route('/sysadmin-users.html', methods = ['GET', 'POST'])
@login_required
def route_sysadmin_users():
    today = time.strftime("%Y-%m-%d", time.localtime())
    log.logger.debug('today is :%s' % today)
    resultstr = oc.fetch('users', '_collection', None, 0, 5)
    log.logger.debug(resultstr)
    return render_template('sysadmin/sysadmin-users.html', segment='sysadmin-users',
                           startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                           today=today)