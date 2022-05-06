#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAdmin
from utils import cryptutil
from utils.pagination import Pagination, get_page_parameter
from apps.sysadmin import blueprint
from flask import render_template, request, url_for, redirect, session
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps import log
import simplejson as json
import time
from decouple import config
from utils.restclient import OSSGPClient


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
    oc = OSSGPClient(session['username'],
                     cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
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
    if request.method == 'GET': #list view delete
        act = request.args.get('act', type=str, default='list')
        page = request.args.get(get_page_parameter(), type=int, default=1)
        if act == 'list':
            count = oc.fetchcount('users')['body']
            perpage = config('OSSGPADMIN_SYS_PAGE_SIZE', default=10, cast=int)
            record = oc.fetch('users', '_collection', None, (page-1)*perpage, perpage)['body']
            pagination = Pagination(page=page, per_page=perpage, total=count, search=False)
            return render_template('sysadmin/sysadmin-users.html', segment='sysadmin-users', act=act,
                                   define = define, record = record, pagination=pagination,
                                   startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                                   today=today)
        elif act == 'create':
            return render_template('sysadmin/sysadmin-users.html', segment='sysadmin-users', act=act,
                                   define=define, page=page,
                                   startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                                   today=today)
        elif act == 'edit':
            key = request.args.get('key', type=str, default=None)
            record = oc.fetchone(key, '_collection/users', None, 0, 5)['body']
            return render_template('sysadmin/sysadmin-users.html', segment='sysadmin-users', act=act,
                                   define=define, page=page, record = record,
                                   startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                                   today=today)
        elif act == 'delete':
            key = request.args.get('key', type=str, default=None)
            record = oc.fetchone(key, '_collection/users', None, 0, 5)['body']
            return render_template('sysadmin/sysadmin-users.html', segment='sysadmin-users', act=act,
                                   define=define, page=page, record = record,
                                   startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                                   today=today)
        else:
            count = oc.fetchcount('users')['body']
            perpage = config('OSSGPADMIN_SYS_PAGE_SIZE', default=10, cast=int)
            record = oc.fetch('users', '_collection', None, (page-1)*perpage, perpage)['body']
            pagination = Pagination(page=page, per_page=perpage, total=count, search=False)
            return render_template('sysadmin/sysadmin-users.html', segment='sysadmin-users', act=act,
                                   define = define, record = record, pagination=pagination,
                                   startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                                   today=today)
    elif request.method == 'POST': # create edit
        act = request.form.get('act', type=str, default='list')
        if act == 'docreate':
            crtjson = {}
            bodyjson = {}
            crtjson['name'] = request.form.get('name')
            crtjson['role'] = request.form.get('role')
            crtjson['password'] = request.form.get('password')
            crtjson['active'] = request.form.get('active', type=bool, default=False)
            bodyjson['data'] = crtjson
            log.logger.debug(bodyjson)
            resultstr = oc.post('users', '_collection', json.dumps(bodyjson))
            page = request.form.get('page', type=int, default=1)
            count = oc.fetchcount('users')['body']
            perpage = config('OSSGPADMIN_SYS_PAGE_SIZE', default=10, cast=int)
            record = oc.fetch('users', '_collection', None, (page - 1) * perpage, perpage)['body']
            pagination = Pagination(page=page, per_page=perpage, total=count, search=False)
            return render_template('sysadmin/sysadmin-users.html', segment='sysadmin-users', act='list',
                                   define=define, record=record, pagination=pagination,
                                   startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                                   today=today)
        elif act == 'doedit':
            crtjson = {}
            bodyjson = {}
            crtjson['name'] = request.form.get('name')
            crtjson['role'] = request.form.get('role')
            crtjson['password'] = request.form.get('password')
            crtjson['active'] = request.form.get('active', type=bool, default=False)
            bodyjson['data'] = crtjson
            key = request.form.get('key')
            resultstr = oc.put('users', '_collection', json.dumps(bodyjson),key)
            page = request.form.get('page', type=int, default=1)
            count = oc.fetchcount('users')['body']
            perpage = config('OSSGPADMIN_SYS_PAGE_SIZE', default=10, cast=int)
            record = oc.fetch('users', '_collection', None, (page - 1) * perpage, perpage)['body']
            pagination = Pagination(page=page, per_page=perpage, total=count, search=False)
            return render_template('sysadmin/sysadmin-users.html', segment='sysadmin-users', act='list',
                                   define=define, record=record, pagination=pagination,
                                   startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                                   today=today)
        elif act == 'dodelete':
            key = request.form.get('key')
            page = request.form.get('page', type=int, default=1)
            perpage = config('OSSGPADMIN_SYS_PAGE_SIZE', default=10, cast=int)
            resultstr = oc.deletebyid('users', '_collection', key)
            count = oc.fetchcount('users')['body']
            if page >= (count//perpage)+1:
                page = (count//perpage)+1
            record = oc.fetch('users', '_collection', None, (page - 1) * perpage, perpage)['body']
            pagination = Pagination(page=page, per_page=perpage, total=count, search=False)
            return render_template('sysadmin/sysadmin-users.html', segment='sysadmin-users', act='list',
                                   define=define, record=record, pagination=pagination,
                                   startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                                   today=today)
        else:
            count = oc.fetchcount('users')['body']
            perpage = config('OSSGPADMIN_SYS_PAGE_SIZE', default=10, cast=int)
            record = oc.fetch('users', '_collection', None, (page-1)*perpage, perpage)['body']
            pagination = Pagination(page=page, per_page=perpage, total=count, search=False)
            return render_template('sysadmin/sysadmin-users.html', segment='sysadmin-users', act=act,
                                   define = define, record = record, pagination=pagination,
                                   startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                                   today=today)


@blueprint.route('/sysadmin-authority.html', methods = ['GET', 'POST'])
@login_required
def route_sysadmin_authority():
    oc = OSSGPClient(session['username'],
                     cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
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
    if request.method == 'GET':  # list
        count = oc.fetchcount('users')['body']
        start = request.args.get('start', type=int)
        length = request.args.get('length', type=int)
        record = oc.fetch('users', '_collection', None, start, length)['body']
        rdata = {
            'data': record['data'],
            'recordsFiltered': record['count'],
            'recordsTotal': count,
            'draw': request.args.get('draw', type=int),
        }
        log.logger.debug("define %s" % define)
        log.logger.debug("rdata %s" % rdata)
        return render_template('sysadmin/sysadmin-authority.html', segment='sysadmin-authority',
                                define=define, record=record,
                                startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                                today=today)

@blueprint.route('/sysadmin-authority/getdata', methods = ['GET', 'POST'])
@login_required
def route_sysadmin_authority_getdata():
    oc = OSSGPClient(session['username'],
                     cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
    if oc.token_expired:
        oc.renew_token()
    if request.method == 'GET':  # list
        count = oc.fetchcount('users')['body']
        start = request.args.get('start', type=int)
        length = request.args.get('length', type=int)
        record = oc.fetch('users', '_collection', None, start, length)['body']
        rdata = {
            'data': record['data'],
            'recordsFiltered': count,
            'recordsTotal': count,
            'draw': request.args.get('draw', type=int),
        }
        log.logger.debug("rdata %s" % rdata)
        return rdata