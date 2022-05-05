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

@blueprint.route('/sysadmin-users.html', methods = ['GET', 'POST'])
@login_required
def route_sysadmin_users():
    if request.method == 'GET': #list view delete
        act = request.args.get('act', type=str, default='list')
        page = request.args.get(get_page_parameter(), type=int, default=1)
        if oc.token_expired:
            oc.renew_token()
        today = time.strftime("%Y-%m-%d", time.localtime())
        definestr = oc.fetch('users', '_sysdef', None, 0, 5)['body']
        define = {}
        define['colname'] = definestr['data'][0]['name']
        define['keyfieldname'] = definestr['data'][0]['keyfieldname']
        define['coldef'] = json.loads(definestr['data'][0]['coldef'])
        thlist = []
        for cdef in define['coldef'].keys():
            if cdef not in ['__collection__', '_index', '_key', 'password']:
                thlist.append(cdef)
        define['thlist'] = thlist
        if act=='list':
            count = oc.fetchcount('users')['body']
            perpage = config('OSSGPADMIN_SYS_PAGE_SIZE', default=10, cast=int)
            record = oc.fetch('users', '_collection', None, (page-1)*perpage, perpage)['body']
            pagination = Pagination(page=page, per_page=perpage, total=count, search=False)
            return render_template('sysadmin/sysadmin-users.html', segment='sysadmin-users', act=act,
                                   define = define, record = record, pagination=pagination,
                                   startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                                   today=today)
        if act=='view':
            key = request.args.get('key', type=str, default=None)
            record = oc.fetchone(key, '_collection/users', None, 0, 5)['body']
            return render_template('sysadmin/sysadmin-users.html', segment='sysadmin-users', act=act,
                                   define=define, page=page, record = record,
                                   startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                                   today=today)

    elif request.method == 'POST': # edit
        pass

@blueprint.route('/sysadmin-authority.html', methods = ['GET', 'POST'])
@login_required
def route_sysadmin_authority():
    if request.method == 'GET':
        if oc.token_expired:
            oc.renew_token()
        today = time.strftime("%Y-%m-%d", time.localtime())
        definestr = oc.fetch('users', '_sysdef', None, 0, 5)['body']
        log.logger.debug('definestr: %s' % definestr)
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
        return render_template('sysadmin/sysadmin-authority.html', segment='sysadmin-authority',
                               define = define, record = record, pagination=pagination,
                               startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                               today=today)
    elif request.method == 'POST':
        pass
