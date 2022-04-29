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
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps import log, oc
import time
from decouple import config


@blueprint.route('/index')
@login_required
def index():
    today = time.strftime("%Y-%m-%d", time.localtime())
    return render_template('home/index.html', segment='index',
                           startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                           today=today)

@blueprint.route('/index.html')
@login_required
def indexhtml():
    today = time.strftime("%Y-%m-%d", time.localtime())
    return render_template('home/index.html', segment='index',
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
        today = time.strftime("%Y-%m-%d", time.localtime())
        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment,
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
