#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAdmin

from utils.pagination import Pagination, get_page_parameter
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

@blueprint.route('/sysadmin-users.html', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def route_sysadmin_users():
    if request.method == 'GET':
        if oc.token_expired:
            oc.renew_token()
        today = time.strftime("%Y-%m-%d", time.localtime())
        definestr = oc.fetch('users', '_sysdef', None, 0, 5)['body']
        count = oc.fetchcount('users')['body']
        page = request.args.get(get_page_parameter(), type=int, default=1)
        perpage = config('OSSGPADMIN_SYS_PAGE_SIZE', default=10, cast=int)
        define = {}
        define['colname'] = definestr['data'][0]['name']
        define['keyfieldname'] = definestr['data'][0]['keyfieldname']
        define['coldef'] = json.loads(definestr['data'][0]['coldef'])
        record = oc.fetch('users', '_collection', None, (page-1)*perpage, perpage)['body']
        #log.logger.debug(definestr)
        #log.logger.debug(define)
        #log.logger.debug(record)
        pagination = Pagination(page=page, per_page=perpage, total=count, search=False)
        return render_template('sysadmin/sysadmin-users.html', segment='sysadmin-users',
                               define = define, record = record, pagination=pagination,
                               startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                               today=today)