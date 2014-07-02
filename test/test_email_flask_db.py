'''
Created on Jun 30, 2014

@author: aljia
'''
import unittest
from src import email_flask_db
import sqlite3

class Test(unittest.TestCase):


    def test_table(self):
        db = sqlite3.connect('db/email_flask.db')
        c= db.cursor()
        c.execute("select tbl_name from sqlite_master")
        self.assertEqual(len(c.fetchall()),2)
        
    def test_insert(self):
        input_msg1 = {
        u'to': u'fake@example.com',
        u'to_name': u'Ms. Fake',
        u'from': u'noreply@uber.com',
        u'from_name': u'Uber',
        u'subject': u'A Message from Uber',
        u'body': u'<h1>Your Bill</h1><p>$10</p>',
        u'text': u'your bill 10 $'
        }
        email_id = email_flask_db.insert('db/email_flask.db', input_msg1, 'accepted')
        db = sqlite3.connect('db/email_flask.db')
        c= db.cursor()
        c.execute("select * from email where id=?", (str(email_id),))
        self.assertEqual(len(c.fetchall()),1)
        c.execute("select * from recipient_email where email_id=?", (str(email_id),))
        self.assertEqual(len(c.fetchall()),1)
       
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
