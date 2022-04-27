# -*- encoding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Scorpius

from flask import Blueprint

blueprint = Blueprint(
    'test_blueprint',
    __name__,
    url_prefix=''
)
