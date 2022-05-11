#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

import asyncio
import distutils
import operator
import os
import traceback

from datetime import datetime, timedelta
import simplejson as json
from pandas import json_normalize

from utils.simple_rest_client.api import API
from env.environment import Environment
from utils import log

'''logging'''
'''logging'''
env = Environment()
log = log.Logger(level=os.getenv('OSSGPADMIN_APP_LOG_LEVEL'))

class OSSGPClient():
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._lastlogin = 0
        self._token_expired = True
        self._access_token = None
        self._token_type = 'bearer'
        httpstr = 'https' if distutils.util.strtobool(os.getenv('OSSGPADMIN_API_USE_HTTPS')) else 'http'
        self._api_root_url = httpstr + '://' + os.getenv('OSSGPADMIN_API_HTTP_HOST') + ':' + os.getenv('OSSGPADMIN_API_HTTPS_PORT') + os.getenv('OSSGPADMIN_API_PREFIX') + '/' if distutils.util.strtobool(os.getenv('OSSGPADMIN_API_USE_HTTPS')) else httpstr + '://' + os.getenv('OSSGPADMIN_API_HTTP_HOST') + ':' + os.getenv('OSSGPADMIN_API_HTTP_PORT') + os.getenv('OSSGPADMIN_API_PREFIX') + '/'
        self._api_client = API(api_root_url = self._api_root_url, params = {}, headers = {}, timeout = int(os.getenv('OSSGPADMIN_API_TIMEOUT')), append_slash = False, json_encode_body = False, ssl_verify=False)


    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def lastlogin(self):
        return self._lastlogin

    @property
    def token_expired(self):
        if self._lastlogin == 0:
            self._token_expired = True
        else:
            self._token_expired = datetime.utcnow() - self._lastlogin > timedelta(minutes=int(os.getenv('OSSGPADMIN_API_TOKEN_EXPIRE_MINUTES')) - 1)
        return self._token_expired

    @property
    def access_token(self):
        return self._access_token

    @property
    def token_type(self):
        return self._token_type

    @property
    def api_root_url(self):
        return self._api_root_url

    def renew_token(self):
        api = self._api_client
        api.add_resource(resource_name='token')
        request_body = {"username": self.username,"password": self.password}
        #log.logger.debug(request_body)
        try:
            response = api.token.create(body = request_body)
            if response.status_code == 200:
                self._access_token = response.body['access_token']
                self._token_type = response.body['token_type']
                self._lastlogin = datetime.utcnow()
            else:
                log.logger.error('Can not get renew_token at renew_token() ... ')
                raise Exception('Can not get renew_token at renew_token()')
        except Exception as exp:
            log.logger.error('Exception at renew_token() %s ' % exp)
            if os.getenv('OSSGPADMIN_APP_EXCEPTION_DETAIL'):
                traceback.print_exc()

    def getuser(self,name):
        action = 'list'
        resource_name = 'users'
        url_prefix = '_collection'
        if name is not None:
            if self.token_expired:
                self.renew_token()
            if (not self.token_expired) and (self.access_token is not None):
                # log.logger.debug('access_token : %s' % self.access_token)
                api = self._api_client
                api.headers = {'Authorization': 'Bearer ' + self.access_token}
                api.api_root_url = self.api_root_url + url_prefix
                api.add_resource(resource_name=resource_name,
                                 full_action_url=api.api_root_url + '/' + resource_name + '/' + name)
                try:
                    res = api._resources[api.correct_attribute_name(resource_name)]
                    func = getattr(res, action)
                    response = func()
                    return response.body
                except Exception as exp:
                    log.logger.error('Exception at getuser() %s ' % exp)
                    if os.getenv('OSSGPADMIN_APP_EXCEPTION_DETAIL'):
                        traceback.print_exc()
                    return None
        else:
            return None

    def user_login(self):
        login_pass = False
        api = self._api_client
        api.add_resource(resource_name='token')
        request_body = {"username": self.username,"password": self.password}
        try:
            response = api.token.create(body = request_body)
            log.logger.debug(response)
            if response.status_code == 200:
                self._access_token = response.body['access_token']
                self._token_type = response.body['token_type']
                self._lastlogin = datetime.utcnow()
                login_pass = True
            else:
                log.logger.error('Can not get user login at user_login() ... ')
        except Exception as exp:
            log.logger.error('Exception at user_login() %s ' % exp)
            if os.getenv('OSSGPADMIN_APP_EXCEPTION_DETAIL'):
                traceback.print_exc()
        return {"result": login_pass, "response": response.body}

    def fetchusers(self):
        api = self._api_client
        api.headers = {'Authorization': 'Bearer ' + self.access_token}
        api.api_root_url = self.api_root_url
        api.add_resource(resource_name='users')
        try:
            response = api.users.list()
            return response.body
        except Exception as exp:
            log.logger.error('Exception at fetchusers() %s ' % exp)
            if os.getenv('OSSGPADMIN_APP_EXCEPTION_DETAIL'):
                traceback.print_exc()

    def fetchcount(self, resource_type, resource_name, url_prefix=''):
        action = 'list'
        if self.token_expired:
            self.renew_token()
        if (not self.token_expired) and (self.access_token is not None):
            api = self._api_client
            api.headers = {'Authorization': 'Bearer ' + self.access_token}
            api.api_root_url = self.api_root_url + '_collection/documentcount/'
            if resource_type == 'sys':
                api.api_root_url = self.api_root_url + '_sysdef/sysdefcount/'
            api.add_resource(resource_name=resource_name)
            try:
                res = api._resources[api.correct_attribute_name(resource_name)]
                func = getattr(res, action)
                response = func()
                res = {'code': response.status_code, 'body': response.body}
                #log.logger.debug("name+count= (%s,%s)" % (resource_name,res))
                return res
            except Exception as exp:
                log.logger.error('Exception at fetchcount() %s ' % exp)
                if os.getenv('OSSGPADMIN_APP_EXCEPTION_DETAIL'):
                    traceback.print_exc()

    def fetch(self, resource_name, url_prefix='', body=None, offset=None, limit=None, sort=None):
        action = 'list'
        if self.token_expired:
            self.renew_token()
        if (not self.token_expired) and (self.access_token is not None):
            # log.logger.debug('access_token : %s' % self.access_token)
            api = self._api_client
            api.headers = {'Authorization': 'Bearer ' + self.access_token}
            if offset is not None:
                api.headers['offset'] = str(offset)
            if limit is not None:
                api.headers['limit'] = str(limit)
            if sort is not None:
                api.headers['sort'] = str(sort)
            api.api_root_url = self.api_root_url + url_prefix
            api.add_resource(resource_name=resource_name)
            try:
                res = api._resources[api.correct_attribute_name(resource_name)]
                #res = api._resources[resource_name]
                #log.logger.debug(res.actions)
                #log.logger.debug(res.get_action_full_url(action))
                #log.logger.debug(res.get_action(action))
                func = getattr(res,action)
                response = None
                if body is not None:
                    response = func(body)
                else:
                    response = func()
                for idict in response.body['data']:
                    idict.update((k, str(v)) for k, v in idict.items())
                res = {'code': response.status_code, 'body': response.body}
                return res
            except Exception as exp:
                log.logger.error('Exception at fetch() %s ' % exp)
                if os.getenv('OSSGPADMIN_APP_EXCEPTION_DETAIL'):
                    traceback.print_exc()

    def fetchone(self, resource_name, url_prefix='', body=None, offset=None, limit=None):
        action = 'list'
        if self.token_expired:
            self.renew_token()
        if (not self.token_expired) and (self.access_token is not None):
            # log.logger.debug('access_token : %s' % self.access_token)
            api = self._api_client
            api.headers = {'Authorization': 'Bearer ' + self.access_token}
            if offset is not None:
                api.headers['offset'] = str(offset)
            if limit is not None:
                api.headers['limit'] = str(limit)
            api.api_root_url = self.api_root_url + url_prefix
            api.add_resource(resource_name=resource_name)
            try:
                res = api._resources[api.correct_attribute_name(resource_name)]
                #res = api._resources[resource_name]
                #log.logger.debug(res.actions)
                #log.logger.debug(res.get_action_full_url(action))
                #log.logger.debug(res.get_action(action))
                func = getattr(res,action)
                response = None
                if body is not None:
                    response = func(body)
                else:
                    response = func()
                #log.logger.debug(response.body)
                idict = response.body.copy()
                idict.update((k, str(v)) for k, v in idict.items())
                res = {'code': response.status_code, 'body': idict}
                return res
            except Exception as exp:
                log.logger.error('Exception at fetchone() %s ' % exp)
                if os.getenv('OSSGPADMIN_APP_EXCEPTION_DETAIL'):
                    traceback.print_exc()

    def post(self, resource_name, url_prefix='', body=None):
        #log.logger.debug(body)
        action = 'create'
        if self.token_expired:
            self.renew_token()
        if (not self.token_expired) and (self.access_token is not None):
            # log.logger.debug('access_token : %s' % self.access_token)
            api = self._api_client
            api.headers = {'Authorization': 'Bearer ' + self.access_token}
            api.api_root_url = self.api_root_url + url_prefix
            api.add_resource(resource_name=resource_name)
            try:
                res = api._resources[api.correct_attribute_name(resource_name)]
                #res = api._resources[resource_name]
                func = getattr(res,action)
                response = None
                if body is not None:
                    response = func(body=body)
                    res = {'code': response.status_code, 'body': response.body}
                else:
                    res = {'code': response.status_code, 'body': response.body}
                return res
            except Exception as exp:
                log.logger.error('Exception at post() %s ' % exp)
                if os.getenv('OSSGPADMIN_APP_EXCEPTION_DETAIL'):
                    traceback.print_exc()

    def put(self, resource_name, url_prefix='', body=None, idvalue=None):
        #log.logger.debug(body)
        action = 'update'
        if self.token_expired:
            self.renew_token()
        if (not self.token_expired) and (self.access_token is not None):
            # log.logger.debug('access_token : %s' % self.access_token)
            api = self._api_client
            api.headers = {'Authorization': 'Bearer ' + self.access_token}
            api.api_root_url = self.api_root_url + url_prefix
            api.add_resource(resource_name=resource_name, full_action_url=api.api_root_url + '/' + resource_name + '/' + idvalue)
            try:
                res = api._resources[api.correct_attribute_name(resource_name)]
                #res = api._resources[resource_name]
                func = getattr(res,action)
                response = None
                if body is not None:
                    response = func(body=body)
                    res = {'code': response.status_code, 'body': response.body}
                else:
                    res = {'code': response.status_code, 'body': response.body}
                return res
            except Exception as exp:
                log.logger.error('Exception at post() %s ' % exp)
                if os.getenv('OSSGPADMIN_APP_EXCEPTION_DETAIL'):
                    traceback.print_exc()

    def deletebyid(self, resource_name, url_prefix='', idvalue=None):
        action = 'destroy'
        if self.token_expired:
            self.renew_token()
        if (not self.token_expired) and (self.access_token is not None):
            # log.logger.debug('access_token : %s' % self.access_token)
            api = self._api_client
            api.headers = {'Authorization': 'Bearer ' + self.access_token}
            api.api_root_url = self.api_root_url + url_prefix
            api.add_resource(resource_name=resource_name, full_action_url=api.api_root_url + '/' + resource_name + '/' + idvalue)
            try:
                res = api._resources[api.correct_attribute_name(resource_name)]
                #res = api._resources[resource_name]
                # log.logger.debug(res.actions)
                # log.logger.debug(res.get_action_full_url(action))
                # log.logger.debug(res.get_action(action))
                func = getattr(res,action)
                response = None
                response = func()
                res = {'code':response.status_code, 'body':response.body}
                return res
            except Exception as exp:
                log.logger.error('Exception at deletebyid() %s ' % exp)
                if os.getenv('OSSGPADMIN_APP_EXCEPTION_DETAIL'):
                    traceback.print_exc()

    def toDataFrame(self, jsonobj, attbname):
        dataframe = json_normalize(jsonobj[attbname])
        return dataframe


if __name__ == '__main__':
    nc = OSSGPClient(os.getenv('OSSGPADMIN_APP_API_USER'), os.getenv('OSSGPADMIN_APP_API_PASSWORD'))
    log.logger.debug(nc.user_login())
    if nc.token_expired:
        nc.renew_token()
    if (not nc.token_expired) and (nc.access_token is not None):
        log.logger.debug(nc.fetchusers())
    log.logger.debug(nc.getuser('admin'))
    log.logger.debug(nc.getuser('ddf'))
    log.logger.debug("nc.getuser('ddf') %s" % nc.getuser('ddf'))
    log.logger.debug(nc.fetchcount('users'))
    resultstr = nc.fetch('users', '_collection', None, 0, 5)
    log.logger.debug(resultstr)
    resultstr = nc.fetch('users', '_collection', None, 0, 5)
    log.logger.debug(resultstr)
    resultstr = nc.fetchone('admin', '_collection/users', None, 0, 5)
    log.logger.debug(resultstr)
    '''
    resultstr = nc.post('users', '_collection', json.dumps({'data': {'name': 'tony', 'password': 'passw0rd', 'role': '[admin,user]', 'active': True}}))
    log.logger.debug(resultstr)
    resultstr = nc.put('users', '_collection', json.dumps({"data": {'name': 'tony2', 'password': 'passw0rd', 'role': '[admin,user]', 'active': True}}),'tony')
    log.logger.debug(resultstr)
    resultstr = nc.deletebyid('users', '_collection', 'tony')
    log.logger.debug(resultstr)
    '''

    '''
    for i in range(100):
        log.logger.debug(str(i))
        resultstr = nc.post('users', '_collection', json.dumps(
            {'data': {'name': 'tony'+str(i), 'password': 'passw0rd', 'role': '[admin,user]', 'active': True}}))
        log.logger.debug(resultstr)
        
        resultstr = nc.deletebyid('users', '_collection', 'tony'+str(i))
        log.logger.debug(resultstr)
    
    if ( not nc.token_expired ) and ( nc.access_token is not None ):
        log.logger.debug(nc.fetchusers())
        ncdb = nc.fetch('database', '_schema')
        log.logger.debug(ncdb)
        ncmeta = nc.fetch('ogdbuser', '_schema/_table')
        log.logger.debug(ncmeta)
        resultstr = nc.fetch('ogdbuser', '_table', None, 0, 5, True)
        log.logger.debug(resultstr)
        table_name = 'ogdbconnect'
        pkname = 'ogdbconnect.ogdb_id'
        spkname = pkname
        if operator.contains(pkname, table_name + '.'):
            spkname = pkname.replace(table_name + '.',"",1)
            #key.strip(table_name + '.')
            #key.replace(table_name + '.',"",1)
        log.logger.debug("spkname: %s" % spkname)
        log.logger.debug("pkname: %s" % pkname)
        log.logger.debug(nc.fetchusers())
        ncdb = nc.fetch('database','_schema')
        log.logger.debug(ncdb)
        ncmeta = nc.fetch('Brands', '_schema/_table')
        log.logger.debug(ncmeta)
        resultstr = nc.fetch('Customer_Ownership','_schema/_table')
        log.logger.debug(resultstr)
        resultstr = nc.fetch('Customer_Ownership', '_table', None, 0, 5, True)
        log.logger.debug(resultstr)
        resultstr = nc.post('Brands', '_table', json.dumps({"data": [{"brand_name":"Mini"}]}))
        log.logger.debug(resultstr)
        resultstr = nc.put('Brands', '_table', json.dumps({"data": {"brand_name": "MG"}, "ids": "brand_id"}), str(resultstr['body']['ids'][0]['brand_id']))
        log.logger.debug(resultstr)
        log.logger.debug(resultstr['body']['brand_id'])
        idfield = 'Customers.id,Customers.id2'
        table_name = 'Customers'
        shortidfield = idfield.replace(table_name+'.','') if operator.contains(idfield,table_name+'.') else idfield
        log.logger.debug(shortidfield)
        idfield = 'id,id2'
        longidfield = idfield if operator.contains(idfield,table_name+'.') else table_name+'.'+(','+table_name+'.').join(idfield.split(','))
        log.logger.debug(longidfield)
        resultstr = nc.deletebyid('Brands', '_table', 'brand_id', str(resultstr['body']['brand_id']))
        log.logger.debug(resultstr)
        idks = ['brand_id']
        ids = [8]
        log.logger.debug(",".join(idks))
        log.logger.debug("-".join(list(map(str, ids))))
    '''