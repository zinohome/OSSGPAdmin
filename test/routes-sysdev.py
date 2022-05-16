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
    nav = get_nav()
    return render_template('sysdev/sysdev.html', segment='sysdev',nav=nav,
                           startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                           today=today)

@blueprint.route('/sysdev-sysdef.html', methods = ['GET', 'POST'])
@login_required
def route_sysdev_sysdef():
    nav = get_nav()
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
    return render_template('sysdev/sysdev-sysdef.html', segment='sysdev-sysdef',nav=nav,
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
            #log.logger.debug(request.form.to_dict())
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
    nav = get_nav()
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
    return render_template('sysdev/sysdev-coldef.html', segment='sysdev-coldef',nav=nav,
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
            #log.logger.debug(request.form.to_dict())
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
    nav = get_nav()
    return render_template('sysdev/sysdev-relation.html', segment='sysdev-relation',nav=nav,
                           startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                           today=today)

@blueprint.route('/sysdev-view.html', methods = ['GET', 'POST'])
@login_required
def route_sysdev_view():
    today = time.strftime("%Y-%m-%d", time.localtime())
    nav = get_nav()
    return render_template('sysdev/sysdev-view.html', segment='sysdev-view',nav=nav,
                           startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                           today=today)

@blueprint.route('/sysdev-adminnav.html', methods = ['GET', 'POST'])
@login_required
def route_sysdev_adminnav():
    today = time.strftime("%Y-%m-%d", time.localtime())
    nav = get_nav()
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
    return render_template('sysdev/sysdev-adminnav.html', segment='sysdev-adminnav',nav=nav,
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
            #log.logger.debug(request.form.to_dict())
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


# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None

# Helper - Generate navigation
def get_nav():
    try:
        nav = []
        oc = OSSGPClient(session['username'],
                         cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
        if oc.token_expired:
            oc.renew_token()
        l1nav = oc.query('adminnav', '_sysdef', None, filter='level==1', filteror=None, sort='order', limit=None,
                         offset=None)
        for l1item in l1nav['body']['data']:
            navitem = {}
            navitem['level'] = 1
            navitem['name'] = l1item['name']
            navitem['title'] = l1item['title']
            navitem['segment'] = l1item['segment']
            navitem['href'] = l1item['href']
            navitem['icon'] = l1item['icon']
            navitem['navclass'] = l1item['navclass']
            #log.logger.debug('l1item: %s' % l1item)
            if l1item['navclass'] == 'sub':
                l2nav = oc.query('adminnav', '_sysdef', None, filter='level==2,order LIKE "'+str(l1item['order'])+'%"', filteror=None, sort='order', limit=None,
                     offset=None)
                sublist = []
                for l2item in l2nav['body']['data']:
                    nav2item = {}
                    nav2item['level'] = 2
                    nav2item['name'] = l2item['name']
                    nav2item['title'] = l2item['title']
                    nav2item['segment'] = l2item['segment']
                    nav2item['href'] = l2item['href']
                    nav2item['icon'] = l2item['icon']
                    nav2item['navclass'] = l2item['navclass']
                    sublist.append(nav2item)
                navitem['sub'] = sublist
                #log.logger.debug('l2nav: %s' % l2nav)
            nav.append(navitem)
        #log.logger.debug('nav: %s' % nav)
        return nav
    except:
        return None
