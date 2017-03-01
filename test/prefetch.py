from swift.common.swob import Response
from swift.common.internal_client import InternalClient
from swiftclient.service import SwiftService, SwiftError
import itertools
from sys import argv
from multiprocessing import Pool
from datetime import datetime as dt
import memcache
import hashlib
import time
import os

OBJ_PATH = '/tmp/log.txt'

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):  # @NoSelf
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
 
class JITDownload(object):
    
    __metaclass__ = Singleton
    
    def __init__(self, global_conf, filter_conf, logger):
        self.logger = logger
        
    def execute(self, req_resp, app_iter, requests_data):
        
        method = requests_data['method']
        if method.upper() == 'GET':
            
            app_iter = self.get_response(req_resp)
            
        return app_iter

    def get_response(self, req_resp):
        print 'BSC test Filter - Object'
        resp_headers = {}   
        resp_headers['content-length'] = str(8071)                
        # resp_headers['etag'] = object_etag
        
        test_object = open(OBJ_PATH,'r')
        
        return Response(app_iter=test_object,
                        headers=resp_headers,
                        request=req_resp) 