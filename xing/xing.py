'''
Created on 04.12.2012

@author: codejitsu, github.com/codejitsu/pyxing
'''
import logging
from globals import api_call_names

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

class Xing(object):
    def __init__(self, consumer_key, consumer_secret, verbose = False, debug = False):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
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
        if self.stack:
            self.__log__('Calling: ' + '/'.join(self.stack))
        else:
            raise XingException('Call stack is empty.', 100) 
        
        return None
    
    def __log__(self, text):
        ''' log the text message to logger or console '''
        
        if self.verbose:
            logger.debug(text)
            
            if self.debug:
                print text                    