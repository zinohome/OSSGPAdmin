#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAPI
import os

from dotenv import load_dotenv


class Environment:
    def __init__(self):
        self.reload()

    def reload(self):
        basepath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        apppath = os.path.abspath(os.path.join(basepath, os.pardir))
        envfilepath = os.path.abspath(os.path.join(apppath, '.env'))
        load_dotenv(dotenv_path=envfilepath, override=True)

if __name__ == '__main__':
    pass