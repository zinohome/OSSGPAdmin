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
from flask import render_template, request, url_for, redirect, session, Response
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
    definestr = oc.fetch('users', '_sysdef/coldef', None, 0, 5)['body']
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
        record = oc.fetch('users', '_collection', None, start, length, 'name')['body']
        rdata = {
            'data': record['data'],
            'recordsFiltered': record['count'],
            'recordsTotal': count,
            'draw': request.args.get('draw', type=int),
        }
        #log.logger.debug("define %s" % define)
        #log.logger.debug("rdata %s" % rdata)
        return render_template('sysadmin/sysadmin-users.html', segment='sysadmin-users',
                                define=define, record=record,
                                startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                                today=today)

@blueprint.route('/sysadmin-users/data', methods = ['GET', 'POST'])
@login_required
def route_sysadmin_users_data():
    oc = OSSGPClient(session['username'],
                     cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
    if oc.token_expired:
        oc.renew_token()
    if request.method == 'GET':  # list
        count = oc.fetchcount('users')['body']
        start = request.args.get('start', type=int)
        length = request.args.get('length', type=int)
        record = oc.fetch('users', '_collection', None, start, length, 'name')['body']
        rdata = {
            'data': record['data'],
            'recordsFiltered': count,
            'recordsTotal': count,
            'draw': request.args.get('draw', type=int),
        }
        return rdata
    elif request.method == 'POST':
        definestr = oc.fetch('users', '_sysdef/coldef', None, 0, 5)['body']
        keyfieldname = definestr['data'][0]['keyfieldname']
        action = request.form.get('action', type=str)
        reqdict = request.form.to_dict()
        formdict = {}
        for (key, value) in reqdict.items():
            if '][' in key:
                formdict[key.split(']')[1][1:]] = value
        formdict['_key'] = formdict[keyfieldname]
        subformdata = {'data':formdict}
        if action == 'create':
            resultstr = oc.post('users', '_collection', json.dumps(subformdata))
            if resultstr['code'] == 200:
                returnlist=[]
                returnlist.append(resultstr['body'])
                returndict={'data':returnlist}
                return Response(json.dumps(returndict), status=200)
            else:
                return Response('{"status":500, "body": "Error"}', status=500)
        elif action == 'edit':
            log.logger.debug(request.form.to_dict())
            resultstr = oc.put('users', '_collection', json.dumps(subformdata),formdict[keyfieldname])
            if resultstr['code'] == 200:
                returnlist=[]
                returnlist.append(resultstr['body'])
                returndict={'data':returnlist}
                return Response(json.dumps(returndict), status=200)
            else:
                return Response('{"status":500, "body": "Error"}', status=500)
        elif action == 'remove':
            resultstr = oc.deletebyid('users', '_collection', formdict[keyfieldname])
            #log.logger.debug(resultstr)
            if resultstr['code'] == 200:
                return Response('{"status":200, "body": "'+ str(resultstr['body'])+'"}', status=200)
            else:
                return Response('{"status":500, "body": "Error"}', status=500)

@blueprint.route('/sysadmin-authority.html', methods = ['GET', 'POST'])
@login_required
def route_sysadmin_authority():
    oc = OSSGPClient(session['username'],
                     cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
    if oc.token_expired:
        oc.renew_token()
    today = time.strftime("%Y-%m-%d", time.localtime())
    definestr = oc.fetch('users', '_sysdef/coldef', None, 0, 5)['body']
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
        record = oc.fetch('users', '_collection', None, start, length, 'name')['body']
        rdata = {
            'data': record['data'],
            'recordsFiltered': record['count'],
            'recordsTotal': count,
            'draw': request.args.get('draw', type=int),
        }
        #log.logger.debug("define %s" % define)
        #log.logger.debug("rdata %s" % rdata)
        return render_template('sysadmin/sysadmin-authority.html', segment='sysadmin-authority',
                                define=define, record=record,
                                startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                                today=today)

@blueprint.route('/sysadmin-authority/data', methods = ['GET', 'POST'])
@login_required
def route_sysadmin_authority_data():
    oc = OSSGPClient(session['username'],
                     cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
    if oc.token_expired:
        oc.renew_token()
    if request.method == 'GET':  # list
        count = oc.fetchcount('users')['body']
        start = request.args.get('start', type=int)
        length = request.args.get('length', type=int)
        record = oc.fetch('users', '_collection', None, start, length, 'name')['body']
        rdata = {
            'data': record['data'],
            'recordsFiltered': count,
            'recordsTotal': count,
            'draw': request.args.get('draw', type=int),
        }
        return rdata
    elif request.method == 'POST':
        definestr = oc.fetch('users', '_sysdef/coldef', None, 0, 5)['body']
        keyfieldname = definestr['data'][0]['keyfieldname']
        action = request.form.get('action', type=str)
        reqdict = request.form.to_dict()
        formdict = {}
        for (key, value) in reqdict.items():
            if '][' in key:
                formdict[key.split(']')[1][1:]] = value
        formdict['_key'] = formdict[keyfieldname]
        subformdata = {'data':formdict}
        if action == 'create':
            resultstr = oc.post('users', '_collection', json.dumps(subformdata))
            if resultstr['code'] == 200:
                returnlist=[]
                returnlist.append(resultstr['body'])
                returndict={'data':returnlist}
                return Response(json.dumps(returndict), status=200)
            else:
                return Response('{"status":500, "body": "Error"}', status=500)
        elif action == 'edit':
            log.logger.debug(request.form.to_dict())
            resultstr = oc.put('users', '_collection', json.dumps(subformdata),formdict[keyfieldname])
            if resultstr['code'] == 200:
                returnlist=[]
                returnlist.append(resultstr['body'])
                returndict={'data':returnlist}
                return Response(json.dumps(returndict), status=200)
            else:
                return Response('{"status":500, "body": "Error"}', status=500)
        elif action == 'remove':
            resultstr = oc.deletebyid('users', '_collection', formdict[keyfieldname])
            #log.logger.debug(resultstr)
            if resultstr['code'] == 200:
                return Response('{"status":200, "body": "'+ str(resultstr['body'])+'"}', status=200)
            else:
                return Response('{"status":500, "body": "Error"}', status=500)