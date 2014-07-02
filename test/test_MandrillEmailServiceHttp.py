'''
Created on Jun 28, 2014

@author: aljia
'''
import unittest
from src.emailservice.MandrillEmailServiceHttp import MandrillEmailServiceHttp
from src.emailservice.config import MandrillEmailServiceHttp_config
import copy
import requests

class TestMandrillEmailServiceHttp(unittest.TestCase):
    
    def test_init(self):
        url_not_str_config = copy.deepcopy(MandrillEmailServiceHttp_config)
        url_not_str_config['key'] = None 
        self.assertRaises(Exception,MandrillEmailServiceHttp, url_not_str_config)
        
        url_empty_str_config = copy.deepcopy(MandrillEmailServiceHttp_config)
        url_empty_str_config['key'] = ''
        self.assertRaises(Exception,MandrillEmailServiceHttp, url_empty_str_config)

        bad_url_config = copy.deepcopy(MandrillEmailServiceHttp_config)
        bad_url_config['url'] = 'https://mandrillapp.com/api'
        self.assertRaises(Exception,MandrillEmailServiceHttp, bad_url_config)
        
        
        bad_key_config = copy.deepcopy(MandrillEmailServiceHttp_config)
        bad_key_config['key'] = '12345678'
        self.assertRaises(Exception,MandrillEmailServiceHttp, bad_key_config)    
        
        
    def test_ping(self):
        config = copy.deepcopy(MandrillEmailServiceHttp_config)
        good_service  =  MandrillEmailServiceHttp(config)
        result =  good_service.ping()
        self.assertIsNone(result)
            

         
        bad_url_config2 = copy.deepcopy(config)
        bad_url_config2['url'] = 'https://mandrillapp.e'
        test_service22  =  MandrillEmailServiceHttp(bad_url_config2)
        result =  test_service22.ping()
        self.assertIsNotNone(result)
        

           
   
         
        timeout_config = copy.deepcopy(config)
        timeout_config['timeout'] = 0.001
        test_service5  =  MandrillEmailServiceHttp(timeout_config)
        result =  test_service5.ping()
        self.assertIsNotNone(result)
        
    def test_build_message(self):
        test_service  =  MandrillEmailServiceHttp(MandrillEmailServiceHttp_config)
    
        input_msg1 = {
            u'to': u'fake@example.com',
            u'to_name': u'Ms. Fake',
            u'from': u'mandrill@uber.com',
            u'from_name': u'Uber',
            u'subject': u'A Message from Uber',
            u'body': u'<h1>Your Bill</h1><p>$10</p>'
            }
        out_msg = test_service.build_message(input_msg1)
        self.assertIsNotNone(out_msg[u'message'][u'html'])
        
        input_msg2 = {
            u'to': u'fake@example.com',
            u'to_name': u'Ms. Fake',
            u'from': u'mandrill@uber.com',
            u'from_name': u'Uber',
            u'subject': u'A Message from Uber',
            u'body': u'<h1>Your Bill</h1>$10</p>'
            }
        out_msg = test_service.build_message(input_msg2)
        self.assertTrue(u'html' not in out_msg[u'message'])
        
        
    def test_send_message(self):
        test_service  =  MandrillEmailServiceHttp(MandrillEmailServiceHttp_config)
        data = {
            u'to': u'yoursyj@gmail.com',
            u'to_name': u'Alex',
            u'from': u'mandrill@uber.com',
            u'from_name': u'Uber',
            u'subject': u'A Test Message from Uber',
            u'body': u'<h1>Your Bill</h1><p>$10</p>'
            }
        payload = test_service.build_message(data);
        result = test_service.send_message(payload)
        self.assertIsInstance(result, requests.Response)
        self.assertEqual(result.status_code, 200)      
        
        data_bad_html = {
            u'to': u'yoursyj@gmail.com',
            u'to_name': u'Alex',
            u'from': u'mandrill@uber.com',
            u'from_name': u'Uber',
            u'subject': u'A Test Message from Uber',
            u'body': u'<h1>Your Bill</h1>$10</p>'
            }
        payload = test_service.build_message(data_bad_html);
        result = test_service.send_message(payload)
        self.assertIsInstance(result, requests.Response)
        self.assertEqual(result.status_code, 200)      
        



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
