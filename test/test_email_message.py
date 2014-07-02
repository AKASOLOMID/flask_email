'''
Created on Jun 27, 2014

@author: aljia
'''
import unittest
from src.email_message import validate_email, validate_name, validate_subject, validate_html, validate_message
import time

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_validate_email(self):
        
        self.assertTrue(validate_email(u'abc@example.com'))
        self.assertTrue(validate_email(u'12.3@example.com'))
        self.assertTrue(validate_email(u'%^&@example.com'))
        self.assertTrue(validate_email(u'name$#{}tag@example.com'))
        self.assertTrue(validate_email(u'"123"@example.com'))
        self.assertTrue(validate_email(u'$A12345@gmail.com'))
        
        
        self.assertFalse(validate_email(None))
        self.assertFalse(validate_email(u''))
        self.assertFalse(validate_email(u'123'))
        self.assertFalse(validate_email(u'/@example'))
        self.assertFalse(validate_email(u'123@45@example.com'))


    def test_validate_name (self):
        self.assertTrue(validate_name(u'abc bca'))
        self.assertTrue(validate_name(u'Ms. Fake fake'))
        self.assertTrue(validate_name(u'Ms. Fake'))
        self.assertTrue(validate_name(u"dr. o'Fake"))
        self.assertTrue(validate_name(u"uber co., ltd"))
        self.assertTrue(validate_name(u"dr. o'Fake"))
        self.assertTrue(validate_name(u"dr. o'Fake"))
        self.assertTrue(validate_name(u"dr. o'Fake"))
        
        self.assertFalse(validate_name(None))  
        self.assertFalse(validate_name(u''))    
        self.assertFalse(validate_name(str(unichr(0))))

    def test_validate_subject(self):
        
        self.assertTrue(validate_subject(u'abc bca'))   
        self.assertFalse(validate_subject(None))      
        self.assertFalse(validate_subject(u''))      
        self.assertFalse(validate_subject(str(unichr(0))))
        
    def test_validate_html(self):
        
        self.assertEqual(validate_html(None)[0], 'error')  
        time.sleep(1)
        self.assertEqual(validate_html('')[0], 'error')
        time.sleep(1)         
        self.assertEqual(validate_html(u'<h1>Your Bill</h1><p>$10</p>')[0], 'passed')  
        time.sleep(1)
        self.assertEqual(validate_html(u'<h1>Your Bill</h1>$10</p>')[0], 'error')
        time.sleep(1) 
        self.assertEqual(validate_html(u'<h1>Your Bill</h1><p>$10')[0], 'passed') 
        time.sleep(1)
        self.assertEqual(validate_html(u'abc')[0], 'error') 
        time.sleep(1)
        self.assertEqual(validate_html(u'<>abc bca')[0], 'error') 
        
         
    def test_validate_message(self):
        self.assertIsNotNone(validate_message('abc'))
        self.assertIsNotNone(validate_message(None))
        valid_msg = {
            u'to': u'fake@example.com',
            u'to_name': u'Ms. Fake',
            u'from': u'noreply@uber.com',
            u'from_name': u'Uber',
            u'subject': u'A Message from Uber',
            u'body': u'<h1>Your Bill</h1><p>$10</p>'
            }
        self.assertIsNone(validate_message(valid_msg))
        
        not_unicode = {
            'to': 'fake@example.com',
            'to_name': 'Ms. Fake',
            'from': 'noreply@uber.com',
            'from_name': 'Uber',
            'subject': 'A Message from Uber',
            'body': '<h1>Your Bill</h1><p>$10</p>'
            }
        self.assertIsNotNone(validate_message(not_unicode))         
        empty_msg ={}
        self.assertIsNotNone(validate_message(empty_msg))
         
        no_to = {u'to_name': u'Ms. Fake',
            u'from': u'noreply@uber.com',
            u'from_name': u'Uber',
            u'subject': u'A Message from Uber',
            u'body': u'<h1>Your Bill</h1><p>$10</p>'}
        self.assertIsNotNone(validate_message(no_to))
 
        no_to_name = {
            u'to': u'fake@example.com',
            u'from': u'noreply@uber.com',
            u'from_name': u'Uber',
            u'subject': u'A Message from Uber',
            u'body': u'<h1>Your Bill</h1><p>$10</p>'
            }
        self.assertIsNotNone(validate_message(no_to_name))
 
        no_from = {
            u'to': u'fake@example.com',
            u'to_name': u'Ms. Fake',
            u'from_name': u'Uber',
            u'subject': u'A Message from Uber',
            u'body': u'<h1>Your Bill</h1><p>$10</p>'
            }
        self.assertIsNotNone(validate_message(no_from))
        no_from_name = {
            u'to': u'fake@example.com',
            u'to_name': u'Ms. Fake',
            u'from': u'noreply@uber.com',
            u'subject': u'A Message from Uber',
            u'body': u'<h1>Your Bill</h1><p>$10</p>'
            }
        self.assertIsNotNone(validate_message(no_from_name))
        no_subject = {
            u'to': u'fake@example.com',
            u'to_name': u'Ms. Fake',
            u'from': u'noreply@uber.com',
            u'from_name': u'Uber',
            u'body': u'<h1>Your Bill</h1><p>$10</p>'
            }
        self.assertIsNotNone(validate_message(no_subject))
         
        no_body= {
            u'to': u'fake@example.com',
            u'to_name': u'Ms. Fake',
            u'from': u'noreply@uber.com',
            u'from_name': u'Uber',
            u'subject': u'A Message from Uber',
            }
        self.assertIsNotNone(validate_message(no_body))  
           
         
        bad_data={u"from": u"Excited User <me@samples.mailgun.org>",
         u"to": u"yoursyj@gmail.com",
         u"subject": u"Helloo",
         u"text": u"Testing some Mailgun awesomness!",
         u"html": u'<h1>Your Bill</h1><p>$10</p>'}
        self.assertIsNotNone(validate_message(bad_data))         

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
