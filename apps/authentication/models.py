#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAdmin
from decouple import config
from flask_login import UserMixin

from apps import login_manager, log

from apps.authentication.util import hash_pass
from utils.restclient import OSSGPClient


class User(UserMixin):
    __collection__ = 'users'
    id = 'null'
    name = 'null'
    password = None
    role = None
    is_active = None

    def __init__(self,username):
        self.username = username
        self.password = None
        self.full_name = None
        self.id = username
        self.role = None
        self.is_active = None
        sc = OSSGPClient(config('OSSGPADMIN_APP_API_USER', default='admin'), config('OSSGPADMIN_APP_API_PASSWORD', default='passw0rd'))
        if sc.token_expired:
            sc.renew_token()
        udict = sc.getuser(username)
        if udict is not None:
            self.id = udict['name']
            self.username = udict['name']
            self.full_name = udict['name']
            self.password = hash_pass(udict['password'])
            self.role = udict['role']
            self.is_active = udict['active']

@login_manager.user_loader
def user_loader(id):
    return User(id)


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = user_loader(username)
    return user
