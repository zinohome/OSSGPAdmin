#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAdmin
from flask_paginate import Pagination, get_page_parameter

from apps.sysadmin import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps import log, oc
import simplejson as json
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
    if oc.token_expired:
        oc.renew_token()
    today = time.strftime("%Y-%m-%d", time.localtime())
    pageinfo = {}
    pageinfo['rcount'] = oc.fetchcount('users')['body']
    pageinfo['rpagesize'] = config('OSSGPADMIN_SYS_PAGE_SIZE', default=10, cast=int)
    pageinfo['rpages'] = pageinfo['rcount'] // pageinfo['rpagesize'] + 1
    pageinfo['curpage'] = 1
    definestr = oc.fetch('users', '_sysdef', None, 0, 5)['body']
    define = {}
    define['colname'] = definestr['data'][0]['name']
    define['keyfieldname'] = definestr['data'][0]['keyfieldname']
    define['coldef'] = json.loads(definestr['data'][0]['coldef'])
    record = oc.fetch('users', '_collection', None, (pageinfo['curpage']-1)*pageinfo['rpagesize'], pageinfo['rpagesize'])['body']
    log.logger.debug(definestr)
    log.logger.debug(define)
    log.logger.debug(record)
    log.logger.debug(pageinfo)
    page = request.args.get(get_page_parameter(), type=int, default=1)

    pagination = Pagination(page=page, total=pageinfo['rcount'], search=False,
                            record_name='record', page_parameter='p',
                            format_total=True, format_number=True)
    log.logger.debug('pagination: %s' % pagination.links)
    #log.logger.debug(page)
    return render_template('sysadmin/sysadmin-users.html', segment='sysadmin-users',
                           define = define, record = record, pageinfo = pageinfo, pagination=pagination,
                           startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                           today=today)