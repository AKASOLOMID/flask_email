'''
Created on Jun 28, 2014

@author: aljia
'''
import requests
from EmailService import EmailService
from src import email_message
import json
import re

class MandrillEmailServiceHttp(EmailService):


    __api_ping = r"users/ping.json"
    __api_send = r'messages/send.json'
    __timeout = 2
   
    
    def __init__(self, config):
        super(EmailService, self).__init__()
   
        if 'url' not in config or type(config['url']) is not  str or len(config['url'])==0:
            raise Exception('MailGunEmailServiceHttp: bad url')
        if 'key' not in config or type(config['key']) is not str or len(config['key'])==0:
            raise Exception('MailGunEmailServiceHttp: bad api')
       
        self.url = config['url']
        self.api_key = config['key']
        self.timeout = MandrillEmailServiceHttp.__timeout
        if 'timeout' in config:
            self.timeout = config['timeout']
        ping_check = self.ping()
        if type(ping_check) is requests.Response:
            raise Exception(ping_check.text)
  
    
                
                
    def ping(self):    
        payload = {'key':self.api_key}
        try:
            response =  requests.get( self.url+'/'+ MandrillEmailServiceHttp.__api_ping, data = json.dumps(payload), timeout=self.timeout) 
            if 200!=response.status_code :          
                return response
        except Exception as e:
            return e
    
    def send_message (self, payload) :
        payload['key']=self.api_key
        try:
            response =  requests.post(self.url+'/'+ MandrillEmailServiceHttp.__api_send,
                data = json.dumps(payload), 
                timeout=self.timeout)
            return response
        except Exception as e:
            return e

    
    def build_message(self,message) :         
        payload = {u'key':self.api_key.decode('unicode_escape'),
                   u'message':{
                       u'from_email': message[u'from'],
                       u'from_name': message[u'from_name'],
                       u'to': [{u'email': message[u'to'], u'name':message[u'to_name'], u'type':u'to'}],
                       u'subject': message[u'subject']
        }}
       
        payload[u'message'][u'text'] =  re.sub(r'<.*?>', '', message[u'body'], flags=re.UNICODE)
        check_html = email_message.validate_html(message[u'body'])
        if 'passed'==check_html[0] or 'warning'==check_html[0]:
            payload[u'message'][u'html'] = message[u'body']
        return payload
        
        
