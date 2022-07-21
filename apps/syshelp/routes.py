#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAdmin

from apps.syshelp import blueprint
from flask import render_template, request, session, Response
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps import log
import simplejson as json
import time
from decouple import config
from apps import cache

from utils import cryptutil
from utils.restclient import OSSGPClient


@blueprint.route('/syshelp-<devname>.html', methods = ['GET', 'POST'])
@login_required
@cache.cached(timeout=600)
def route_syshelp(devname):
    today = time.strftime("%Y-%m-%d", time.localtime())
    nav = get_nav()
    pgdef = get_pagedef(devname)
    define = get_sysdef(devname)
    if not (pgdef is None or define is None):
        for etfield in pgdef['pagedef']['et_fields']:
            if etfield['type'] == 'jsoneditor':
                define['has_jsoneditor'] = True
                define['jsoneditor_options'] = etfield['options']
                define['jsoneditor_def'] = etfield['def']
                break
        define['pagedef'] = pgdef
        #log.logger.debug(define)
        #log.logger.debug(define['pagedef'])
        return render_template('syshelp/syshelp.html', segment='syshelp-'+devname, nav=nav,
                               define=define,devname=devname,
                               startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                               today=today)
    else:
        return render_template('home/page-404.html'), 404

@blueprint.route('/syshelp-<devname>/data', methods = ['GET', 'POST'])
@login_required
def route_syshelp_data(devname):
    oc = OSSGPClient(session['username'],
                     cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
    if oc.token_expired:
        oc.renew_token()
    pgdef = get_pagedef(devname)
    if pgdef is None:
        return Response('{"status":500, "body": "Error"}', status=500)
    else:
        if request.method == 'GET':  # list
            count = oc.fetchcount('sys', devname)['body']
            start = request.args.get('start', type=int)
            length = request.args.get('length', type=int)
            record = oc.fetch(devname, '_sysdef', None, start, length, pgdef['pagedef']['dt_order'])['body']
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
            defname = 'coldef' if devname == 'sysdef' else devname
            definestr = oc.fetch(defname, '_sysdef/sysdef', None, 0, 5)['body']
            keyfieldname = definestr['keyfieldname']
            action = request.form.get('action', type=str)
            reqdict = request.form.to_dict()
            formdict = {}
            for (key, value) in reqdict.items():
                if '][' in key:
                    formdict[key.split(']')[1][1:]] = value
            formdict['_key'] = formdict[keyfieldname]
            subformdata = {'data':formdict}
            if action == 'create':
                resultstr = oc.post(devname, '_sysdef', json.dumps(subformdata))
                if resultstr['code'] == 200:
                    returnlist=[]
                    returnlist.append(resultstr['body'])
                    returndict={'data':returnlist}
                    return Response(json.dumps(returndict), status=200)
                else:
                    return Response('{"status":500, "body": "Error"}', status=500)
            elif action == 'edit':
                #log.logger.debug(request.form.to_dict())
                resultstr = oc.put(devname, '_sysdef', json.dumps(subformdata),formdict[keyfieldname])
                if resultstr['code'] == 200:
                    returnlist=[]
                    returnlist.append(resultstr['body'])
                    returndict={'data':returnlist}
                    return Response(json.dumps(returndict), status=200)
                else:
                    return Response('{"status":500, "body": "Error"}', status=500)
            elif action == 'remove':
                resultstr = oc.deletebyid(devname, '_sysdef', formdict[keyfieldname])
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

@cache.memoize(timeout=30)
def get_sysdef(devname):
    try:
        # sysdef define same with coldef
        oc = OSSGPClient(session['username'],
                         cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
        if oc.token_expired:
            oc.renew_token()
        defname = 'coldef' if devname == 'sysdef' else devname
        definestr = oc.fetch(defname, '_sysdef/sysdef', None, 0, 5)['body']
        define = {}
        define['colname'] = devname
        define['keyfieldname'] = definestr['keyfieldname']
        define['coldef'] = json.loads(definestr['coldef'])
        thlist = []
        for cdef in define['coldef'].keys():
            if cdef not in ['__collection__', '_index', '_key', 'password']:
                thlist.append(cdef)
        define['thlist'] = thlist
        define['has_jsoneditor'] = False
        return define
    except:
        return None

@cache.memoize(timeout=30)
def get_all_pagetitle(devname):
    try:
        oc = OSSGPClient(session['username'],
                         cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
        if oc.token_expired:
            oc.renew_token()
        pages = oc.fetch('pagedef', '_sysdef', body=None, offset=None,
                             limit=config('OSSGPADMIN_API_QUERY_LIMIT_UPSET', default='2000'), sort='name')['body']
        pagetitle = {}
        for page in pages['data']:
            pagetitle[page['name']] = json.loads(page['pagedef'])['block_title']
        return pagetitle
    except:
        return None

@cache.memoize(timeout=30)
def get_pagedef(devname):
    try:
        oc = OSSGPClient(session['username'],
                         cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
        if oc.token_expired:
            oc.renew_token()
        modelnames = oc.fetch('sysdef', '_sysdef/sysdefnames', body=None, offset=None,
                              limit=config('OSSGPADMIN_API_QUERY_LIMIT_UPSET', default='2000'), sort='name')['body']
        modelnames.append('sysdef') if not 'sysdef' in set(modelnames) else None
        if devname in set(modelnames):
            pagenames = oc.fetch('pagedef', '_sysdef/sysdefnames', body=None, offset=None,
                                 limit=config('OSSGPADMIN_API_QUERY_LIMIT_UPSET', default='2000'), sort='name')['body']
            if devname in set(pagenames):
                result = oc.fetch(devname, '_sysdef/pagedef', body=None, offset=None,
                                  limit=config('OSSGPADMIN_API_QUERY_LIMIT_UPSET', default='2000'))['body']
                result['pagedef'] = json.loads(result['pagedef'])
                return result
            else:
                return None
        else:
            return None
    except:
        return None

# Helper - Generate navigation
@cache.cached(timeout=600, key_prefix='get_nav')
def get_nav():
    try:
        nav = []
        oc = OSSGPClient(session['username'],
                         cryptutil.decrypt(config('OSSGPADMIN_APP_SECRET', default='bgt56yhn'), session['password']))
        if oc.token_expired:
            oc.renew_token()
        l1nav = oc.query('navdef', '_sysdef', None, filter='level==1', filteror=None, sort='order', limit=None,
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
                l2nav = oc.query('navdef', '_sysdef', None, filter='level==2,order LIKE "'+str(l1item['order'])+'%"', filteror=None, sort='order', limit=None,
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
