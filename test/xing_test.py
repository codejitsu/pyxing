'''
Created on 04.12.2012

@author: codejitsu, github.com/codejitsu/pyxing
'''

import unittest
from xing.xing import Xing

class Test(unittest.TestCase):    
    def setUp(self):
        self.xing = Xing('my_key', 'my_secret', True, True)
            
    def testMe(self):        
        self.assertIsNotNone(self.xing.users.me(), 'me() should return a not None value.')
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()