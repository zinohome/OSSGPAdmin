#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAdmin

from apps.home import blueprint
from flask import render_template, request, session
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps import log
import time
from decouple import config

from utils import cryptutil
from utils.restclient import OSSGPClient


@blueprint.route('/index')
@login_required
def index():
    today = time.strftime("%Y-%m-%d", time.localtime())
    nav = get_nav()
    return render_template('home/index.html', segment='index', nav = nav,
                           startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                           today=today)

@blueprint.route('/index.html')
@login_required
def indexhtml():
    today = time.strftime("%Y-%m-%d", time.localtime())
    nav = get_nav()
    return render_template('home/index.html', segment='index', nav = nav,
                           startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                           today=today)


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'
        # Detect the current page
        segment = get_segment(request)
        nav = get_nav()
        today = time.strftime("%Y-%m-%d", time.localtime())
        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment, nav = nav,
                               startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                               today=today)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


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
