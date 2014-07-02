'''
Created on Jun 26, 2014

@author: aljia
'''

import sys, os
import unittest
from src.emailservice.MailGunEmailServiceHttp import MailGunEmailServiceHttp
from src.emailservice.config import MailGunEmailServiceHttp_config
import copy
import requests



class TestMailGunEmailServiceHttp(unittest.TestCase):


    def test_init(self):
        url_not_str_config = copy.deepcopy(MailGunEmailServiceHttp_config)
        url_not_str_config['url'] = None 
        self.assertRaises(Exception,MailGunEmailServiceHttp, url_not_str_config)
        
        url_empty_str_config = copy.deepcopy(MailGunEmailServiceHttp_config)
        url_empty_str_config['url'] = ''
        self.assertRaises(Exception,MailGunEmailServiceHttp, url_empty_str_config)
        
        bad_url_config = copy.deepcopy(MailGunEmailServiceHttp_config)
        bad_url_config['url'] = 'https://api.mailgun.net'
        self.assertRaises(Exception,MailGunEmailServiceHttp, bad_url_config)
     
        
        bad_key_config = copy.deepcopy(MailGunEmailServiceHttp_config)
        bad_key_config['key'] = '12345678'
        self.assertRaises(Exception,MailGunEmailServiceHttp, bad_key_config)
           
        bad_domain_config = copy.deepcopy(MailGunEmailServiceHttp_config)
        bad_domain_config['domain'] = '12345678'
        self.assertRaises(Exception,MailGunEmailServiceHttp, bad_domain_config)
        
    def test_ping(self):
        config = copy.deepcopy(MailGunEmailServiceHttp_config)
        test_service1  =  MailGunEmailServiceHttp(config)
        result =  test_service1.ping()
        self.assertIsNone(result)
           

         
        bad_url_config2 = copy.deepcopy(config)
        bad_url_config2['url'] = 'https://api.mailgun'
        test_service22  =  MailGunEmailServiceHttp(bad_url_config2)
        result =  test_service22.ping()
        self.assertIsNotNone(result)
        

         
        timeout_config = copy.deepcopy(config)
        timeout_config['timeout'] = 0.001
        test_service5  =  MailGunEmailServiceHttp(timeout_config)
        result =  test_service5.ping()
        self.assertIsNotNone(result)


         

    def test_build_message(self):
        test_service  =  MailGunEmailServiceHttp(MailGunEmailServiceHttp_config)
    
        input_msg1 = {
            u'to': u'fake@example.com',
            u'to_name': u'Ms. Fake',
            u'from': u'noreply@uber.com',
            u'from_name': u'Uber',
            u'subject': u'A Message from Uber',
            u'body': u'<h1>Your Bill</h1><p>$10</p>'
            }
        expected_result1 = {u'to': u'Ms. Fake <fake@example.com>', u'text': u'Your Bill$10', u'html': u'<h1>Your Bill</h1><p>$10</p>', u'from': u'Uber <noreply@uber.com>', u'subject': u'A Message from Uber'}
        self.assertTrue(test_service.build_message(input_msg1)==expected_result1)
        
        input_msg2 = {
            u'to': u'fake@example.com',
            u'to_name': u'Ms. Fake',
            u'from': u'noreply@uber.com',
            u'from_name': u'Uber',
            u'subject': u'A Message from Uber',
            u'body': u'<h1>Your Bill</h1>$10</p>'
            }
        expected_result2 = {u'to': u'Ms. Fake <fake@example.com>', u'text': u'Your Bill$10',  u'from': u'Uber <noreply@uber.com>', u'subject': u'A Message from Uber'}
        self.assertTrue(test_service.build_message(input_msg2)==expected_result2)
       
    def test_send_message(self):
        test_service  =  MailGunEmailServiceHttp(MailGunEmailServiceHttp_config)
        data = {
            u'to': u'yoursyj@gmail.com',
            u'to_name': u'Alex',
            u'from': u'mailgun@uber.com',
            u'from_name': u'Uber',
            u'subject': u'A Test Message from Uber',
            u'body': u'<h1>Your Bill</h1><p>$10</p>'
            }
        payload = test_service.build_message(data);
        result = test_service.send_message(payload)
        self.assertIsInstance(result, requests.Response)
        self.assertEqual(result.status_code, 200)       
          
        test_service  =  MailGunEmailServiceHttp(MailGunEmailServiceHttp_config)
        bad_html = {
            u'to': u'yoursyj@gmail.com',
            u'to_name': u'Alex',
            u'from': u'mailgun@uber.com',
            u'from_name': u'Uber',
            u'subject': u'A Test Message from Uber',
            u'body': u'<h1>Your Bill</h1>$10</p>'
            }
        payload = test_service.build_message(bad_html);
        result = test_service.send_message(payload)
        self.assertIsInstance(result, requests.Response)
        self.assertEqual(result.status_code, 200)   
        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
   
    unittest.main()
    

    
