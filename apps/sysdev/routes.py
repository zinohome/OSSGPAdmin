#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAdmin

from apps.sysdev import blueprint
from flask import render_template, request, session, Response
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps import log
import simplejson as json
import time
from decouple import config

from utils import cryptutil
from utils.restclient import OSSGPClient


@blueprint.route('/sysdev.html', methods = ['GET', 'POST'])
@login_required
def route_sysdev():
    today = time.strftime("%Y-%m-%d", time.localtime())
    return render_template('sysdev/sysdev.html', segment='sysdev',
                           startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                           today=today)

@blueprint.route('/sysdev-sysdef.html', methods = ['GET', 'POST'])
@login_required
def route_sysdev_sysdef():
    today = time.strftime("%Y-%m-%d", time.localtime())
    oc = OSSGPClient(session['username'],
                     cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
    if oc.token_expired:
        oc.renew_token()
    today = time.strftime("%Y-%m-%d", time.localtime())
    #sysdef define same with coldef
    definestr = oc.fetch('coldef', '_sysdef/sysdef', None, 0, 5)['body']
    define = {}
    define['colname'] = definestr['data'][0]['name']
    define['keyfieldname'] = definestr['data'][0]['keyfieldname']
    define['coldef'] = json.loads(definestr['data'][0]['coldef'])
    thlist = []
    for cdef in define['coldef'].keys():
        if cdef not in ['__collection__', '_index', '_key', 'password']:
            thlist.append(cdef)
    define['thlist'] = thlist
    return render_template('sysdev/sysdev-sysdef.html', segment='sysdev-sysdef',
                            define=define,
                            startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                            today=today)

@blueprint.route('/sysdev-sysdef/data', methods = ['GET', 'POST'])
@login_required
def route_sysadmin_sysdef_data():
    oc = OSSGPClient(session['username'],
                     cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
    if oc.token_expired:
        oc.renew_token()
    if request.method == 'GET':  # list
        count = oc.fetchcount('sys', 'sysdef')['body']
        start = request.args.get('start', type=int)
        length = request.args.get('length', type=int)
        record = oc.fetch('sysdef', '_sysdef', None, start, length, 'name')['body']
        rdata = {
            'data': record['data'],
            'recordsFiltered': count,
            'recordsTotal': count,
            'draw': request.args.get('draw', type=int),
        }
        #log.logger.debug("rdata %s" % rdata)
        return rdata
    elif request.method == 'POST':
        # sysdef define same with coldef
        definestr = oc.fetch('coldef', '_sysdef/sysdef', None, 0, 5)['body']
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
            resultstr = oc.post('sysdef', '_sysdef', json.dumps(subformdata))
            if resultstr['code'] == 200:
                returnlist=[]
                returnlist.append(resultstr['body'])
                returndict={'data':returnlist}
                return Response(json.dumps(returndict), status=200)
            else:
                return Response('{"status":500, "body": "Error"}', status=500)
        elif action == 'edit':
            log.logger.debug(request.form.to_dict())
            resultstr = oc.put('sysdef', '_sysdef', json.dumps(subformdata),formdict[keyfieldname])
            if resultstr['code'] == 200:
                returnlist=[]
                returnlist.append(resultstr['body'])
                returndict={'data':returnlist}
                return Response(json.dumps(returndict), status=200)
            else:
                return Response('{"status":500, "body": "Error"}', status=500)
        elif action == 'remove':
            resultstr = oc.deletebyid('sysdef', '_sysdef', formdict[keyfieldname])
            #log.logger.debug(resultstr)
            if resultstr['code'] == 200:
                return Response('{"status":200, "body": "'+ str(resultstr['body'])+'"}', status=200)
            else:
                return Response('{"status":500, "body": "Error"}', status=500)

@blueprint.route('/sysdev-coldef.html', methods = ['GET', 'POST'])
@login_required
def route_sysdev_coldef():
    today = time.strftime("%Y-%m-%d", time.localtime())
    oc = OSSGPClient(session['username'],
                     cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
    if oc.token_expired:
        oc.renew_token()
    today = time.strftime("%Y-%m-%d", time.localtime())
    definestr = oc.fetch('coldef', '_sysdef/sysdef', None, 0, 5)['body']
    define = {}
    define['colname'] = definestr['data'][0]['name']
    define['keyfieldname'] = definestr['data'][0]['keyfieldname']
    define['coldef'] = json.loads(definestr['data'][0]['coldef'])
    thlist = []
    for cdef in define['coldef'].keys():
        if cdef not in ['__collection__', '_index', '_key', 'password']:
            thlist.append(cdef)
    define['thlist'] = thlist
    return render_template('sysdev/sysdev-coldef.html', segment='sysdev-coldef',
                            define=define,
                            startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                            today=today)

@blueprint.route('/sysdev-coldef/data', methods = ['GET', 'POST'])
@login_required
def route_sysadmin_coldef_data():
    oc = OSSGPClient(session['username'],
                     cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
    if oc.token_expired:
        oc.renew_token()
    if request.method == 'GET':  # list
        count = oc.fetchcount('sys', 'coldef')['body']
        start = request.args.get('start', type=int)
        length = request.args.get('length', type=int)
        record = oc.fetch('coldef', '_sysdef', None, start, length, 'name')['body']
        rdata = {
            'data': record['data'],
            'recordsFiltered': count,
            'recordsTotal': count,
            'draw': request.args.get('draw', type=int),
        }
        #log.logger.debug("rdata %s" % rdata)
        return rdata
    elif request.method == 'POST':
        definestr = oc.fetch('coldef', '_sysdef/sysdef', None, 0, 5)['body']
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
            resultstr = oc.post('coldef', '_sysdef', json.dumps(subformdata))
            if resultstr['code'] == 200:
                returnlist=[]
                returnlist.append(resultstr['body'])
                returndict={'data':returnlist}
                return Response(json.dumps(returndict), status=200)
            else:
                return Response('{"status":500, "body": "Error"}', status=500)
        elif action == 'edit':
            log.logger.debug(request.form.to_dict())
            resultstr = oc.put('coldef', '_sysdef', json.dumps(subformdata),formdict[keyfieldname])
            if resultstr['code'] == 200:
                returnlist=[]
                returnlist.append(resultstr['body'])
                returndict={'data':returnlist}
                return Response(json.dumps(returndict), status=200)
            else:
                return Response('{"status":500, "body": "Error"}', status=500)
        elif action == 'remove':
            resultstr = oc.deletebyid('coldef', '_sysdef', formdict[keyfieldname])
            #log.logger.debug(resultstr)
            if resultstr['code'] == 200:
                return Response('{"status":200, "body": "'+ str(resultstr['body'])+'"}', status=200)
            else:
                return Response('{"status":500, "body": "Error"}', status=500)

@blueprint.route('/sysdev-relation.html', methods = ['GET', 'POST'])
@login_required
def route_sysdev_relation():
    today = time.strftime("%Y-%m-%d", time.localtime())
    return render_template('sysdev/sysdev-relation.html', segment='sysdev-relation',
                           startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                           today=today)

@blueprint.route('/sysdev-view.html', methods = ['GET', 'POST'])
@login_required
def route_sysdev_view():
    today = time.strftime("%Y-%m-%d", time.localtime())
    return render_template('sysdev/sysdev-view.html', segment='sysdev-view',
                           startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                           today=today)

@blueprint.route('/sysdev-adminnav.html', methods = ['GET', 'POST'])
@login_required
def route_sysdev_adminnav():
    today = time.strftime("%Y-%m-%d", time.localtime())
    oc = OSSGPClient(session['username'],
                     cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
    if oc.token_expired:
        oc.renew_token()
    today = time.strftime("%Y-%m-%d", time.localtime())
    definestr = oc.fetch('adminnav', '_sysdef/sysdef', None, 0, 5)['body']
    define = {}
    define['colname'] = definestr['data'][0]['name']
    define['keyfieldname'] = definestr['data'][0]['keyfieldname']
    define['coldef'] = json.loads(definestr['data'][0]['coldef'])
    thlist = []
    for cdef in define['coldef'].keys():
        if cdef not in ['__collection__', '_index', '_key', 'password']:
            thlist.append(cdef)
    define['thlist'] = thlist
    return render_template('sysdev/sysdev-adminnav.html', segment='sysdev-adminnav',
                           define=define,
                           startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                           today=today)

@blueprint.route('/sysdev-adminnav/data', methods = ['GET', 'POST'])
@login_required
def route_sysadmin_adminnav_data():
    oc = OSSGPClient(session['username'],
                     cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
    if oc.token_expired:
        oc.renew_token()
    if request.method == 'GET':  # list
        count = oc.fetchcount('sys', 'adminnav')['body']
        start = request.args.get('start', type=int)
        length = request.args.get('length', type=int)
        record = oc.fetch('adminnav', '_sysdef', None, start, length, 'order')['body']
        rdata = {
            'data': record['data'],
            'recordsFiltered': count,
            'recordsTotal': count,
            'draw': request.args.get('draw', type=int),
        }
        #log.logger.debug("rdata %s" % rdata)
        return rdata
    elif request.method == 'POST':
        definestr = oc.fetch('adminnav', '_sysdef/sysdef', None, 0, 5)['body']
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
            resultstr = oc.post('adminnav', '_sysdef', json.dumps(subformdata))
            if resultstr['code'] == 200:
                returnlist=[]
                returnlist.append(resultstr['body'])
                returndict={'data':returnlist}
                return Response(json.dumps(returndict), status=200)
            else:
                return Response('{"status":500, "body": "Error"}', status=500)
        elif action == 'edit':
            log.logger.debug(request.form.to_dict())
            resultstr = oc.put('adminnav', '_sysdef', json.dumps(subformdata),formdict[keyfieldname])
            if resultstr['code'] == 200:
                returnlist=[]
                returnlist.append(resultstr['body'])
                returndict={'data':returnlist}
                return Response(json.dumps(returndict), status=200)
            else:
                return Response('{"status":500, "body": "Error"}', status=500)
        elif action == 'remove':
            resultstr = oc.deletebyid('adminnav', '_sysdef', formdict[keyfieldname])
            #log.logger.debug(resultstr)
            if resultstr['code'] == 200:
                return Response('{"status":200, "body": "'+ str(resultstr['body'])+'"}', status=200)
            else:
                return Response('{"status":500, "body": "Error"}', status=500)
