'''
Created on Jun 30, 2014

@author: aljia
'''
import unittest
import email_flask
from db import db_schema
import os
import json
import app_config


post_data = data = {
            u'to': u'yoursyj@gmail.com',
            u'to_name': u'Alex',
            u'from': u'mandrill@uber.com',
            u'from_name': u'Uber',
            u'subject': u'A Test Message from emai_flask',
            u'body': u'<h1>you got the email</h1><p>awesome</p>'
            }
class Test(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.app = email_flask.app
        self.client = self.app.test_client()
        self.app.config.from_object(app_config.TestingConfig)
        db_schema.create_db(self.app.config['DATABASE_URI'])
        
    @classmethod
    def tearDownClass(self):
        os.remove(self.app.config['DATABASE_URI'])
        
        
    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_home_page(self):
        rv = self.client.get('/')
        assert 'email form' in rv.data

    def test_post(self):
        headers = [('Content-Type', 'application/json')]
        rv = self.client.post('/', data=json.dumps(post_data), headers=headers)
        self.assertEqual(rv.status_code,200)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
