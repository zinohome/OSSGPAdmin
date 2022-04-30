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
    pageinfo = {}
    pageinfo['rcount'] = oc.fetchcount('users')['body']
    pageinfo['rpagesize'] = config('OSSGPADMIN_SYS_PAGE_SIZE', default=10, cast=int)
    pageinfo['rpages'] = pageinfo['rcount'] // pageinfo['rpagesize'] + 1
    pageinfo['curpage'] = 1
    define = oc.fetch('users', '_sysdef', None, 0, 5)
    record = oc.fetch('users', '_collection', None, (pageinfo['curpage']-1)*pageinfo['rpagesize'], pageinfo['rpagesize'])
    log.logger.debug(define['body'])
    log.logger.debug(record['body'])
    log.logger.debug(pageinfo)
    return render_template('sysadmin/sysadmin-users.html', segment='sysadmin-users',
                           define = define['body'], record = record['body'], pageinfo = pageinfo,
                           startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                           today=today)