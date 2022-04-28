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
        self._curpage = 1
        self._pagesize = 10
        '''OSSGPClient'''
        self.oc = OSSGPClient(os.getenv('OSSGPADMIN_APP_SYS_USER'), os.getenv('OSSGPADMIN_APP_SYS_PASSWORD'))
        '''table_columns'''
        self.table_columns = [
            {'title': '用户名', 'dataIndex': 'name'},
            {'title': '用户角色', 'dataIndex': 'role'},
            {'title': '激活', 'dataIndex': 'active'}
        ]
        '''card title & id'''
        self.card_title = 'UsersCard'
        self.table_title = 'UsersTable'
        self.table_id = 'userstable'

    def users_page(self):
        return [
            Card(title=self.card_title,
                 content = [
                DataTable(title=self.table_title,
                          columns=self.table_columns,
                          data=TableResult(self.oc.fetch(self._collname, '_collection', None, None, 20)['body']['data'], self.oc.fetchcount(self._collname)['body']),
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
                id=self.table_id
            )
        ]

    def users_on_page(self,query):
        log.logger.debug("=================== users_on_page ===================")
        self._curpage = query['current_page']
        self._pagesize = query['page_size']
        return TableResult(self.oc.fetch(self._collname, '_collection', None, (self._curpage-1)*self._pagesize, self._pagesize)['body']['data'], self.oc.fetchcount(self._collname)['body'], self._curpage, self._pagesize)

    def users_on_new(self):
        print('new users')

    def users_on_view(self,item):
        log.logger.debug("=================== users_on_view ===================")
        return ReplaceElement(self.table_id, Card(
            title=self.card_title,
            content=[
                DetailGroup('用户信息', content=[
                    DetailItem('name', str(item['name'])),
                    DetailItem('role', str(item['role'])),
                    DetailItem('active', str(item['active'])),
                ]),
                Divider(),
                Button(title='返回', style='primary', on_click=self.users_back_view, id='users_return')
            ],
            id=self.table_id
        ))

    def users_on_edit(self,item):
        print(item)

    def users_back_view(self):
        return ReplaceElement(self.table_id, Card(title=self.card_title,
                content = [
                DataTable(title=self.table_title,
                          columns=self.table_columns,
                          data=TableResult(self.oc.fetch(self._collname, '_collection', None, (self._curpage-1)*self._pagesize, self._pagesize)['body']['data'], self.oc.fetchcount(self._collname)['body'], self._curpage, self._pagesize),
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
                id=self.table_id
            )
        )

    def users_on_delete(self,item):
        print(item)
