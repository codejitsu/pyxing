'''
Created on 04.12.2012

@author: codejitsu, github.com/codejitsu/pyxing
'''

from test.oauth_keys import consumer_key, consumer_secret, oauth_token, \
    oauth_token_secret
from xing.xing import Xing, XingException
import unittest

'''
User Profiles:
--------------
x GET     /v1/users/:id
x GET     /v1/users/me
GET     /v1/users/me/id_card
GET     /v1/users/find_by_emails

Contacts:
---------
x GET     /v1/users/:user_id/contacts
GET     /v1/users/:user_id/contacts/:contact_id/tags
GET     /v1/users/:user_id/contacts/shared
'''

class XingApiTest(unittest.TestCase):    
    def setUp(self):        
        self.xing = Xing(consumer_key, consumer_secret, oauth_token, oauth_token_secret, '1')
            
    def testMe(self):        
        ''' test call to /users/me '''
        self.assertIsNotNone(self.xing.users.me.get(), 'me() should return a not None value.')

    def testMeResponseCode200(self):        
        ''' test call to /users/me '''
        self.xing.users.me.get()
        self.assertEqual(self.xing.http_status, '200', 'me() should return http 200 code. Was %s.' % (self.xing.http_status,))

    def testStackShouldBeEmptyAfterCall(self):        
        ''' test call to /users/me '''
        self.xing.users.me.get()
        self.assertFalse(self.xing.stack, 'stack should be empty.')
    
    def testNotExistingApiCall(self):
        ''' test call to not existing api '''
        with self.assertRaises(XingException) as cm:
            self.xing.blah.blah.get()
            the_exception = cm.exception
            self.assertEqual(the_exception.code, 101)

    def testStackShouldBeEmptyAfterException(self):
        ''' test call to not existing api '''        
        with self.assertRaises(XingException) as cm:
            self.xing.blah.blah.get()
            the_exception = cm.exception
            self.assertEqual(the_exception.code, 101)
            self.assertFalse(self.xing.stack, 'stack should be empty.')
    
    def testMeContacts(self):
        ''' test call to /users/me/contacts '''
        self.assertIsNotNone(self.xing.users('me').contacts.get(), 'me/contacts() should return a not None value.')
        self.assertEqual(self.xing.http_status, '200', 'me/contacts() should return http 200 code. Was %s.' % (self.xing.http_status,))
    
    def testMeContactsContent(self):
        ''' Get the part of my contact list. '''
        contacts = self.xing.users.me.contacts.get()
    
        if contacts and contacts['contacts']['users']:
            for c in contacts['contacts']['users']:
                contact = self.xing.users(c['id']).get()
                
                if contact:
                    self.assertEqual(c['id'], contact['users'][0]['id'], 'Contact id not the same.')
    
    def testMeContactsWithParameters(self):
        ''' Get the part of my contact list. '''
        contacts = self.xing.users.me.contacts.get()
    
        if contacts and contacts['contacts']['users']:
            for c in contacts['contacts']['users']:
                contact = self.xing.users(c['id']).get(fields = 'display_name,photo_urls,id')
                
                if contact:
                    self.assertEqual(c['id'], contact['users'][0]['id'], 'Contact id not the same.')
                    self.assertFalse('professional_experience' in contact['users'][0], 'professional_experience should not be in the result dict.')                    
                    self.assertFalse('educational_background' in contact['users'][0], 'educational_background should not be in the result dict.')
                        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()