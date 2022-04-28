#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2022 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2022
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Scorpius - OSSGPAdmin
import json
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

'''table_columns'''
table_columns = [
    {'title': '用户名', 'dataIndex': 'name'},
    {'title': '用户角色', 'dataIndex': 'role'},
    {'title': '激活', 'dataIndex': 'active'}
]

'''page & size'''
curpage = 0
curpagesize = 0

def users_page():
    return [
        Card(title='UsersTable',
             content = [
            DataTable("UsersTable",
                      columns=table_columns,
                      data=TableResult(oc.fetch('users', '_collection', None, None, 20)['body']['data'], oc.fetchcount('users')['body']),
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
    curpage = query['current_page']
    curpagesize = query['page_size']
    return TableResult(oc.fetch('users', '_collection', None, (query['current_page']-1)*query['page_size'], query['page_size'])['body']['data'], oc.fetchcount('users')['body'], query['current_page'], query['page_size'])

def users_on_new():
    print('new users')

def users_on_view(item):
    log.logger.debug("=================== users_on_page ===================")
    #{'__collection__': 'users', 'active': True, 'name': 'tony4', 'password': 'passw0rd', 'role': '[admin,user]'}
    log.logger.debug(item)
    log.logger.debug(item['name'])
    return ReplaceElement('userstable', Card(
        title='userstable',
        content=[
            DetailGroup('用户信息', content=[
                DetailItem('name', str(item['name'])),
                DetailItem('role', str(item['role'])),
                DetailItem('active', str(item['active'])),
            ]),
            Divider(),
            Button('Navigate to details', on_click=users_back_view),
        ],
        id='userstable'
    ))

def users_on_edit(item):
    print(item)

def users_back_view():
    return ReplaceElement('userstable', Card(title='UsersTable',
            content = [
            DataTable("UsersTable",
                      columns=table_columns,
                      data=TableResult(oc.fetch('users', '_collection', None, (curpage-1)*curpagesize, curpagesize)['body']['data'], oc.fetchcount('users')['body']),
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
    )

def users_on_delete(item):
    print(item)
