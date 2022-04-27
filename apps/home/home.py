#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Scorpius - OSSGPAdmin

from utils.adminui import *

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