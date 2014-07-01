'''
Created on Jun 28, 2014

@author: aljia
'''

import string
import importlib
import requests

from src.emailservice import config
import email_message
        
class EmailHandler(object):
    
    config = config

    def __init__(self):
        
        self.service_list = []
        self.default_service = 0;
   
        for item in dir(EmailHandler.config) :
            if item.startswith("__"):
                continue
            try:
                service_name = item[:-7]
                service_module = importlib.import_module('.'+service_name, string.rsplit(config.__name__,'.',1)[0])
                service_def = getattr(service_module,service_name)
                service_config = getattr(EmailHandler.config, service_name+'_config')
                service_instance= service_def(service_config)   
            except Exception as e :
                continue
            self.service_list.append(service_instance)                

            if 'default' in service_config :
                self.default_service = len(self.service_list) -1;        
                
        if len(self.service_list)==0:
            raise Exception('no running service found')

  
    
    def send_message(self, message):
        check_msg = email_message.validate_message(message)
        if check_msg is not None :
            return check_msg
        
        for idx in range(self.default_service - len(self.service_list), self.default_service):
            payload = self.service_list[idx].build_message(message)
            rsp = self.service_list[idx].send_message(payload)
            if type(rsp) is requests.Response and rsp.status_code==200 :
                return rsp
        
        return 'no service is available'
            
        
        
