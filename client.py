'''
Created on 05.12.2012

@author: codejitsu, github.com/codejitsu/pyxing
'''

from xing import xing
from test.oauth_keys import consumer_key, consumer_secret, oauth_token,\
    oauth_token_secret

if __name__ == '__main__':
    xing = xing.Xing(consumer_key, consumer_secret, oauth_token, oauth_token_secret, '1')
    
    print 'Calling users.me:'
    me_response = xing.users.me.get()
    
    print 'Me: %s %s' % (me_response['users'][0]['first_name'], me_response['users'][0]['last_name'],)
    print

    print 'Get my contacts:'
    
    contacts = xing.users.me.contacts.get()
    
    if contacts and contacts['contacts']['users']:
        for c in contacts['contacts']['users']:
            contact = xing.users(c['id']).get(fields = 'display_name,photo_urls,id')
            
            if contact:
                print 'Contact: id = %s, name = %s' % (c['id'], contact['users'][0]['display_name'])
            