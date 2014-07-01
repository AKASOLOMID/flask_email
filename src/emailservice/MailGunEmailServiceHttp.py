import requests
from  EmailService import EmailService
from src import email_message
import re
class MailGunEmailServiceHttp(EmailService):
    
    __api_send = 'messages'
    __timeout = 2
   
    
    def __init__(self, config):
        super(EmailService, self).__init__()
 
        if 'url' not in config or type(config['url']) is not str or len(config['url'])==0:
            raise Exception('MailGunEmailServiceHttp: bad url')
        if 'key' not in config or type(config['key']) is not str or len(config['key'])==0:
            raise Exception('MailGunEmailServiceHttp: bad api')
        if 'domain' not in config or type(config['domain']) is not str or len(config['domain'])==0:
            raise Exception('MailGunEmailServiceHttp: bad domain')
        self.url = config['url']
        self.api_key = config['key']
        self.domain = config['domain']
        self.timeout = MailGunEmailServiceHttp.__timeout
        if 'timeout' in config:
            self.timeout = config['timeout']
        ping_check = self.ping()
        if type(ping_check) is requests.Response:
            raise Exception(ping_check.text)
            
                
                
    def ping(self):    
        try:
            response =  requests.get( self.url+'/'+self.domain+'/log',auth=('api', self.api_key), timeout=self.timeout) 
            if 200!=response.status_code :
                return response
        except Exception as e:
     
            return e
    
    def send_message (self, payload) :
        try:
            response =  requests.post( self.url+'/'+self.domain+'/'+MailGunEmailServiceHttp.__api_send,
                auth=('api', self.api_key), 
                data = payload, 
                timeout=self.timeout)
            return response
        except Exception as e:
            return e

    
    def build_message(self,message) :       
        payload=dict()
        payload[u'from'] = message[u'from_name'] + u' <' + message[u'from'] + u'>'
        payload[u'to'] = message[u'to_name'] + u' <' + message[u'to'] + u'>'
        payload[u'subject'] = message[u'subject']
        
        check_html = email_message.validate_html(message[u'body'])
        payload[u'text'] =  re.sub(r'<.*?>', '', message[u'body'], flags=re.UNICODE)
        if 'passed'==check_html[0] or 'warning'==check_html[0]:
            payload[u'html'] = message[u'body']
        return payload
        

        

