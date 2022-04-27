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
    return [
        Card(content=[
            Header('Header of the record', 1),
            DetailGroup('Refund Request', content=[
                DetailItem('Order No.', 1100000),
                DetailItem('Status', "Fetched"),
                DetailItem('Shipping No.', 1234567),
                DetailItem('Sub Order', 1135456)
            ]),
            Divider(),
            DetailGroup('User Info', content=[
                DetailItem('Name', "Alice"),
                DetailItem('Phone', "555-123-4567"),
                DetailItem('Shipping Service', 'Continent Ex'),
                DetailItem('Address', 'XXX XXXX Dr. XX-XX, XXXXXX NY 12345'),
                DetailItem('Remarks', "None")
            ]),
        ])
    ]

# blueprint
for module_name in ('test',):
    module = importlib.import_module('apps.{}.routes'.format(module_name))
    app.app.register_blueprint(module.blueprint)

log.logger.debug(app.url_map)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='9000',debug=True)