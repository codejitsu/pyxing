'''
Created on 04.12.2012

@author: codejitsu, github.com/codejitsu/pyxing
'''
import logging

logger = logging.getLogger(__name__)

class XingException(Exception):
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
        
        if self.verbose:
            text = 'Put ' + name + ' on the top of the call stack.'
            logger.debug(text)
            
            if self.debug:
                print text
            
        self.stack.append(name)
                
        return self
    
    def __call__(self):
        if self.stack:
            if self.verbose:
                text = 'calling: ' + '/'.join(self.stack)
                logger.debug(text)
                
                if self.debug:
                    print text            
        else:
            raise XingException('Call stack is empty.', 100) 
        
        return None