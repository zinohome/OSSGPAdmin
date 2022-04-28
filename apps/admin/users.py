#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Scorpius - OSSGPAdmin
import os

from utils.adminui import *
from env.environment import Environment
from utils import log
from utils.restclient import OSSGPClient

'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPADMIN_APP_LOG_LEVEL'))

'''OSSGPClient'''
oc = OSSGPClient(os.getenv('OSSGPADMIN_APP_SYS_USER'), os.getenv('OSSGPADMIN_APP_SYS_PASSWORD'))

def users_page():
    table_columns = [
        {'title': '用户名', 'dataIndex': 'name'},
        {'title': '用户角色', 'dataIndex': 'role'},
        {'title': '激活', 'dataIndex': 'active'}
    ]
    ocresult = oc.fetch('users', '_collection', None, None, None)
    log.logger.debug(ocresult)
    return [
        Card(title='UsersTable',
             content = [
            DataTable("UsersTable",
                      columns=table_columns,
                      data=TableResult(ocresult['body']['data'], ocresult['body']['count']),
                      on_data=users_on_page,
                      row_actions=[
                          TableRowAction('view', '查看', on_click=users_on_view),
                          TableRowAction('edit', '修改', on_click=users_on_edit),
                          TableRowAction('delete', '删除', on_click=users_on_delete),
                      ],
                      table_actions=[
                          Button(title='新增', style='primary', on_click=users_on_new, id='users_add'),
                      ]
                      )],
            id='userstable'
        )
    ]

def users_on_page(query):
    log.logger.debug("=================== users_on_page ===================")
    ocresult = oc.fetch('users', '_collection', None, (query['current_page']-1)*query['page_size'], query['page_size'])
    log.logger.debug(ocresult)
    return TableResult(ocresult['body']['data'], ocresult['body']['count'], query['current_page'])

def users_on_new():
    print('new users')

def users_on_view(item):
    return ReplaceElement('userstable', Card(
        title='UsersContant',
        content=[
            Header('Header 1', 1),
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
            Divider(),
            Header('Header 1', 1),
            Header('Header 2', 2),
            Header('Header 3', 3),
            Header('Header 4', 4),
            Paragraph("a red paragraph", color='red'),
            RawHTML('a raw <font color="red">HTML</font>'),
            Paragraph("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore\n magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.\n Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        ],
        id='userscontant'
    ))

def users_on_edit(item):
    print(item)

def users_on_delete(item):
    print(item)
