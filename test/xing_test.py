'''
Created on 04.12.2012

@author: codejitsu, github.com/codejitsu/pyxing
'''

from test.oauth_keys import consumer_key, consumer_secret, oauth_token, \
    oauth_token_secret
from xing.xing import Xing, XingException
import unittest

class XingApiTest(unittest.TestCase):    
    def setUp(self):        
        self.xing = Xing(consumer_key, consumer_secret, oauth_token, oauth_token_secret, '1', True, True)
            
    def testMe(self):        
        ''' test call to /users/me '''
        self.assertIsNotNone(self.xing.users.me(), 'me() should return a not None value.')

    def testMeResponseCode200(self):        
        ''' test call to /users/me '''
        resp = self.xing.users.me()[0]['status']
        self.assertEqual(resp, '200', 'me() should return http 200 code. Was %s.' % (resp,))

    def testStackShouldBeEmptyAfterCall(self):        
        ''' test call to /users/me '''
        self.xing.users.me()
        self.assertFalse(self.xing.stack, 'stack should be empty.')
    
    def testNotExistingApiCall(self):
        ''' test call to not existing api '''
        with self.assertRaises(XingException) as cm:
            self.xing.blah.blah()
            the_exception = cm.exception
            self.assertEqual(the_exception.code, 101)

    def testStackShouldBeEmptyAfterException(self):
        ''' test call to not existing api '''        
        with self.assertRaises(XingException) as cm:
            self.xing.blah.blah()
            the_exception = cm.exception
            self.assertEqual(the_exception.code, 101)
            self.assertFalse(self.xing.stack, 'stack should be empty.')
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()