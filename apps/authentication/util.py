#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: OSSGPAdmin

import os
import hashlib
import binascii
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password):
    return pwd_context.hash(password)


def verify_pass(provided_password, stored_password):
    return pwd_context.verify(provided_password, stored_password)
