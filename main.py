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
from apps.admin import admin, users
from apps.about import about
from utils.restclient import OSSGPClient

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPADMIN_APP_LOG_LEVEL'))

app = AdminApp()
app.app_title = "Practitioner"
app.set_menu(
    [
        MenuItem('首页', '/', icon="dashboard"),
        MenuItem('工作台', '/user_home', icon="dashboard", auth_needed='user', children=[
            MenuItem('New Item', '/new', icon="plus"),
            MenuItem('Search for Item', '/search', icon="search", auth_needed='admin'),
            MenuItem('Admin', '/admin', icon="setting")
        ]),
        MenuItem('设置', '/', icon="dashboard", auth_needed='admin', children=[
            MenuItem('New Item', '/new', icon="plus"),
            MenuItem('用户管理', '/users', icon="search"),
            MenuItem('系统配置', '/admin', icon="setting")
        ]),
        MenuItem('系统帮助', '/about', icon="info-circle")
    ]
)

@app.login()
def on_login(username, password):
    oc = OSSGPClient(username, password)
    loginresponse = oc.user_login()
    if loginresponse['result']:
        payload = jwt.decode(loginresponse['response']['access_token'], os.getenv("OSSGPADMIN_API_AUTH_SECURITY_KEY"), os.getenv("OSSGPADMIN_API_AUTH_SECURITY_ALGORITHM"))
        #log.logger.debug(payload)
        return LoggedInUser(payload.get("name"), payload.get("role"), redirect_to='/') # you can optionally return roles of the user
    else:
        return LoginFailed()

@app.page('/', 'Home Page', auth_needed='user')
def home_page():
    return home.home_page()


@app.page('/admin', 'Admin', auth_needed='admin')
def admin_page():
    return admin.admin_page()

@app.page('/users', 'Users', auth_needed='admin')
def users_page():
    return users.users_page()

@app.page('/about', 'About', auth_needed='user')
def about_page():
    return about.about_page()



if __name__ == '__main__':
    app.run(host='0.0.0.0',port='6890',debug=True)