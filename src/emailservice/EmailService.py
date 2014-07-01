from abc import ABCMeta
from abc import abstractmethod





class EmailService(object):

    __metaclass__ = ABCMeta
    

    
    @abstractmethod
    def __init__(self, config):
        pass
        

    @abstractmethod
    def send_message (self, payload): 
        pass
    


    @abstractmethod
    def ping(self) : 
        pass
    
    @abstractmethod
    def build_message(self,message) : 
        pass

    