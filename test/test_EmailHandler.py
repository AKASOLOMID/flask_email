'''
Created on Jun 29, 2014

@author: aljia
'''
import unittest
import requests

from src.EmailHandler import EmailHandler
import config_empty
import config_reject_enroll
import config_no_default
import config_default
from src.emailservice import config


class TestEmailHandler(unittest.TestCase):

    def tearDown(self):
        EmailHandler.config = config

    def test_init(self):
        EmailHandler.config=config_empty
        self.assertRaises(Exception, EmailHandler)
        
        EmailHandler.config=config
        eh = EmailHandler()
        self.assertEqual(len(eh.service_list), 2)
        self.assertEqual(eh.default_service, 0)

        EmailHandler.config=config_no_default
        eh = EmailHandler()
        self.assertEqual(len(eh.service_list), 2)
        self.assertEqual(eh.default_service, 0)

        EmailHandler.config=config_default
        eh = EmailHandler()
        self.assertEqual(len(eh.service_list), 2)
        self.assertEqual(eh.default_service, 1)

        EmailHandler.config=config_reject_enroll
        eh = EmailHandler()
        self.assertEqual(len(eh.service_list), 1)
        self.assertEqual(eh.default_service, 0)
        

    def test_send_message(self):
        EmailHandler.config=config_default
        eh = EmailHandler()   
        valid_msg = {
            u'to': u'yoursyj@gmail.com',
            u'to_name': u'Ms. Fake',
            u'from': u'noreply@uber.com',
            u'from_name': u'Uber',
            u'subject': u'A Message from Uber',
            u'body': u'<h1>Your Bill</h1><p>$10</p>'
        }
        response = eh.send_message(valid_msg)
        self.assertIsInstance(response, requests.Response)
        self.assertEqual(response.status_code, 200) 
        url = response.url.encode('ascii', 'ignore')
        url2 = config_default.MandrillEmailServiceHttp_config['url']
        self.assertEqual(url[:len(url2)], url2)
           
    def test_switch_service(self):
        EmailHandler.config=config
        eh = EmailHandler() 
        self.assertEqual(len(eh.service_list), 2)
        self.assertEqual(eh.default_service, 0)  
        key_cp = eh.service_list[0].api_key
        eh.service_list[0].api_key = 'invalid key'
        valid_msg = {
            u'to': u'yoursyj@gmail.com',
            u'to_name': u'Ms. Fake',
            u'from': u'noreply@uber.com',
            u'from_name': u'Uber',
            u'subject': u'A Message from Uber',
            u'body': u'<h1>Your Bill</h1><p>$10</p>'
        }
        response = eh.send_message(valid_msg)
        self.assertIsInstance(response, requests.Response)
        self.assertEqual(response.status_code, 200) 
        url = response.url.encode('ascii', 'ignore')
        url2 = config_default.MandrillEmailServiceHttp_config['url']
        self.assertEqual(url[:len(url2)], url2)
         
        eh.service_list[0].api_key = key_cp
        eh.service_list[1].api_key = 'invalid key'      
        response = eh.send_message(valid_msg)
        self.assertIsInstance(response, requests.Response)
        self.assertEqual(response.status_code, 200) 
        url = response.url.encode('ascii', 'ignore')
        url2 = config_default.MailGunEmailServiceHttp_config['url']
        self.assertEqual(url[:len(url2)], url2)   



  
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
