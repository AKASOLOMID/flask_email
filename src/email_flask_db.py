'''
Created on Jun 30, 2014

@author: aljia
'''

import datetime
import sqlite3






def insert(path, message, state):
    db = sqlite3.connect(path)
    try:
        c = db.cursor()
        c.execute(u"""insert into email(id,from_address, from_name, subject, body, state, time) values (null,?,?,?,?,?,?)""",
            (message[u'from'], message[u'from_name'],message[u'subject'],message[u'body'], str(state).decode('unicode_escape'),
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")  ))
        email_id = c.lastrowid
        c.execute(u"""insert into recipient_email(email_id, to_address, to_name, to_type, time) values(?,?,?,?,?)""",
            (email_id, message[u'to'], message[u'to_name'], 'to',  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")))
      
        db.commit()
        return email_id
    finally:
        db.close()

