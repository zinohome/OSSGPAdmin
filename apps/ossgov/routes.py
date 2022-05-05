#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAdmin

from apps.ossgov import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps import log
import time
from decouple import config

@blueprint.route('/ossgov.html', methods = ['GET', 'POST'])
@login_required
def route_ossgov():
    today = time.strftime("%Y-%m-%d", time.localtime())
    return render_template('ossgov/ossgov.html', segment='ossgov',
                           startdate=config('OSSGPADMIN_SYS_START_DAY', default='2020-02-19'),
                           today=today)
