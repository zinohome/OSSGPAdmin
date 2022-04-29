#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAdmin

from flask_login import UserMixin

from apps import login_manager, log, oc

from apps.authentication.util import hash_pass

class User(UserMixin):
    __collection__ = 'users'
    id = 'null'
    name = 'null'
    password = None
    role = None
    is_active = None

    def __init__(self, name):
        udict = oc.getuser(name)
        if udict is not None:
            self.id = udict['name']
            self.name = udict['name']
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
