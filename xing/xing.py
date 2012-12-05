'''
Created on 04.12.2012

@author: codejitsu, github.com/codejitsu/pyxing
'''
from globals import api_call_names
import logging
import oauth2 as oauth
import time

logger = logging.getLogger(__name__)

class XingException(Exception):
    '''
    100 - call stack is empty
    101 - call to not existing api
    '''
    def __init__(self, msg, code):
        self.msg = msg
        self.code = code
        
    def __str__(self):
        return 'Xing Exception: %s Exception Code: %i' % (self.msg, self.code)

class XingHttpException(Exception):
    ''' All http errors. '''
    pass

class Xing(object):
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret, version = '1', verbose = False, debug = False):
        self.api_version = version
        self.site = 'https://api.xing.com'
        self.format = 'json'
        
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret
        self.verbose = verbose
        self.debug = debug
        self.stack = []
        
    def __getattr__(self, name):
        ''' Put the name on the top of call stack. '''
        
        if name.lower() not in api_call_names:
            self.__log__('Calling not existing api %s' % (name.lower(),))
                            
            raise XingException('Call to not existing api %s' % (name,), 101)
        
        if self.verbose:
            self.__log__('Put ' + name + ' on the top of the call stack.')
            
        self.stack.append(name)
                
        return self
    
    def __call__(self):
        try:
            if self.stack:
                self.__log__('Calling: ' + '/'.join(self.stack))
                
                url = self.__make_request_url__()
                
                params = {
                    'oauth_version': "1.0",
                    'oauth_nonce': oauth.generate_nonce(),
                    'oauth_timestamp': int(time.time())
                }
                
                token = oauth.Token(key = self.access_token, secret = self.access_secret)
                consumer = oauth.Consumer(key = self.consumer_key, secret = self.consumer_secret)
                
                params['oauth_token'] = token.key
                params['oauth_consumer_key'] = consumer.key
                
                req = oauth.Request(method="GET", url=url, parameters=params)
                
                # Sign the request.
                signature_method = oauth.SignatureMethod_HMAC_SHA1()
                req.sign_request(signature_method, consumer, token)            
                
                client = oauth.Client(consumer)
                
                resp = client.request(req.to_url())
                
                self.__log__(resp)
                
                return resp
            else:
                raise XingException('Call stack is empty.', 100) 
        finally:
                self.stack = []
            
        return None
    
    def __make_request_url__(self):
        first_part = '%s/v%s/' % (self.site, self.api_version,)
        return first_part + '/'.join(self.stack) + '.' + self.format 
                
    def __log__(self, text):
        ''' log the text message to logger or console '''
        
        if self.verbose:
            logger.debug(text)
            
            if self.debug:
                print text                    