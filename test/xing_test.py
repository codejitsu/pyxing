'''
Created on 04.12.2012

@author: codejitsu, github.com/codejitsu/pyxing
'''

import unittest
from xing.xing import Xing, XingException

class XingApiTest(unittest.TestCase):    
    def setUp(self):
        self.xing = Xing('my_key', 'my_secret', True, True)
            
    def testMe(self):        
        ''' test call to /users/me '''
        self.assertIsNotNone(self.xing.users.me(), 'me() should return a not None value.')
    
    def testNotExistingApiCall(self):
        ''' test call to not existing api '''
        with self.assertRaises(XingException) as cm:
            self.xing.blah.blah()
            the_exception = cm.exception
            self.assertEqual(the_exception.code, 101)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()