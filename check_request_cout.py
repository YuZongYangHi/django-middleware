#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.core.cache import cache
from django.http import HttpResponseForbidden
import redis

request_count = 0 
expire_timer = 60 

class CheckMaliceClientMiddleWare:
    def __init__(self,get_response):
        self.get_response = get_response
        self.poll  = redis.ConnectionPool(host='127.0.0.1')
        self.redis = redis.Redis(connection_pool=self.poll)

    def __call__(self,request):
        source_ip =  request.META['REMOTE_ADDR']
        if self.redis.llen(source_ip) >= request_count:
             return HttpResponseForbidden('<h1>Forbidden Your Access Many</h1>')
        self.redis.expire(source_ip,expire_timer);
        self.redis.lpush(source_ip,'handler')
        response = self.get_response(request)
        return response
