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

def admin_page():
    table_columns = [
        {'title': 'Rule Name', 'dataIndex': 'name'},
        {'title': 'Description', 'dataIndex': 'desc'},
        {'title': '# of Calls', 'dataIndex': 'callNo'},
        {'title': 'Status', 'dataIndex': 'status'},
        {'title': 'Updated At', 'dataIndex': 'updatedAt'}
    ]
    table_data = [{"callNo": 76,"desc": "Description of Operation","id": 0,"name": "Alpha","status": 3,"updatedAt": "2019-12-13"}]
    return [
        Card(content = [
            DataTable("Example Table", columns=table_columns,
                data=TableResult(table_data))])
    ]