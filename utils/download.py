from swift.common.swob import Response
from swift.common.internal_client import InternalClient
from swiftclient.service import SwiftService, SwiftError
from sys import argv
import hashlib
import time
import os

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

        time.sleep(0.01)
        return req_resp.environ['wsgi.input']
