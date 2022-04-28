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

class UsersView(object):
    def __init__(self):
        self._collname = 'users'
        '''page & size'''
        self._curpage = 0
        self._pagesize = 0
        '''OSSGPClient'''
        self.oc = OSSGPClient(os.getenv('OSSGPADMIN_APP_SYS_USER'), os.getenv('OSSGPADMIN_APP_SYS_PASSWORD'))
        '''table_columns'''
        self.table_columns = [
            {'title': '用户名', 'dataIndex': 'name'},
            {'title': '用户角色', 'dataIndex': 'role'},
            {'title': '激活', 'dataIndex': 'active'}
        ]
        '''card title & id'''
        self.card_title = 'UsersTable'
        self.card_id = 'userstable'

    def users_page(self):
        return [
            Card(title=self.card_title,
                 content = [
                DataTable(title=self.card_title,
                          columns=self.table_columns,
                          data=TableResult(self.oc.fetch('users', '_collection', None, None, 20)['body']['data'], self.oc.fetchcount('users')['body']),
                          on_data=self.users_on_page,
                          row_actions=[
                              TableRowAction('view', '查看', on_click=self.users_on_view),
                              TableRowAction('edit', '修改', on_click=self.users_on_edit),
                              TableRowAction('delete', '删除', on_click=self.users_on_delete),
                          ],
                          table_actions=[
                              Button(title='新增', style='primary', on_click=self.users_on_new, id='users_add'),
                          ]
                          )],
                id=self.card_id
            )
        ]

    def users_on_page(self,query):
        log.logger.debug("=================== users_on_page ===================")
        self.curpage = query['current_page']
        self.pagesize = query['page_size']
        return TableResult(self.oc.fetch('users', '_collection', None, (self.curpage-1)*self.pagesize, self.pagesize)['body']['data'], self.oc.fetchcount('users')['body'], self.curpage, self.pagesize)

    def users_on_new(self):
        print('new users')

    def users_on_view(self,item):
        log.logger.debug("=================== users_on_page ===================")
        return ReplaceElement(self.card_id, Card(
            title=self.card_title,
            content=[
                DetailGroup('用户信息', content=[
                    DetailItem('name', str(item['name'])),
                    DetailItem('role', str(item['role'])),
                    DetailItem('active', str(item['active'])),
                ]),
                Divider(),
                Button('Navigate to details', on_click=self.users_back_view),
            ],
            id=self.card_id
        ))

    def users_on_edit(self,item):
        print(item)

    def users_back_view(self):
        return ReplaceElement(self.card_id, Card(title=self.card_title,
                content = [
                DataTable(title=self.card_title,
                          columns=self.table_columns,
                          data=TableResult(self.oc.fetch('users', '_collection', None, (self.curpage-1)*self.pagesize, self.pagesize)['body']['data'], self.oc.fetchcount('users')['body']),
                          on_data=self.users_on_page,
                          row_actions=[
                              TableRowAction('view', '查看', on_click=self.users_on_view),
                              TableRowAction('edit', '修改', on_click=self.users_on_edit),
                              TableRowAction('delete', '删除', on_click=self.users_on_delete),
                          ],
                          table_actions=[
                              Button(title='新增', style='primary', on_click=self.users_on_new, id='users_add'),
                          ]
                          )],
                id=self.card_id
            )
        )

    def users_on_delete(self,item):
        print(item)
