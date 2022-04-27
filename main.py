#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Scorpius - OSSGPAdmin
import importlib
import os

from env.environment import Environment
from utils.adminui import *
from utils import log
from apps.home import home
from apps.admin import admin
from apps.about import about

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPADMIN_APP_LOG_LEVEL'))

app = AdminApp()
app.app_title = "Scorpius"
app.set_menu(
    [
        MenuItem('Home', '/', icon="dashboard"),
        MenuItem('User Home', '/user_home', icon="dashboard", auth_needed='user', children=[
            MenuItem('New Item', '/new', icon="plus"),
            MenuItem('Search for Item', '/search', icon="search", auth_needed='admin'),
            MenuItem('Admin', '/admin', icon="setting")
        ]),
        MenuItem('Admin Only', '/', icon="dashboard", auth_needed='admin', children=[
            MenuItem('New Item', '/new', icon="plus"),
            MenuItem('Search for Item', '/search', icon="search"),
            MenuItem('Admin', '/admin', icon="setting")
        ]),
        MenuItem('About', '/about', icon="info-circle")
    ]
)

@app.login()
def on_login(username, password):
    if username=='alice' and password=='123456':
        return LoggedInUser("Alice", ['user', 'manager'], redirect_to='/') # you can optionally return roles of the user
    else:
        return LoginFailed()

@app.page('/', 'Home Page', auth_needed='user')
def home_page():
    return home.home_page()

@app.page('/admin', 'Admin', auth_needed='user')
def admin_page():
    return admin.admin_page()

@app.page('/about', 'About', auth_needed='user')
def about_page():
    return about.about_page()



if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9000',debug=True)