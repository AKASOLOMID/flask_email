'''
Created on Jun 28, 2014

@author: aljia
'''
from string import printable
import re
from py_w3c.validators.html.validator import HTMLValidator

html_template_head = u"""<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head><title>I AM YOUR DOCUMENT TITLE REPLACE ME</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><meta http-equiv="Content-Style-Type" content="text/css">
</head><body>
 """
html_template_tail =u'</body></html>'  



# validate all fields in the message except body
def validate_message(msg):
    if type(msg) is not dict:
        return 'message is not type of dictionary'
 
  
    if u'to' not in msg:
        return 'no recipient email address found\n'
    elif not validate_email(msg[u'to']) :
        return'invalid recipient email address\n'
 
    if u'to_name' not in msg:
        return'no recipient name found\n'
    elif not validate_name(msg[u'to_name']) :
        return'invalid recipient name\n'
 
    if u'from' not in msg:
        return'no sender email address found\n'
    elif not validate_email(msg[u'from']) :
        return'invalid sender email address\n' 
    if u'from_name' not in msg:
        return'no sender name found\n'
    elif not validate_name(msg[u'from_name']) :
        return'invalid sender name\n'
         
    if u'subject' not in msg:
        return'no subject found\n'
    elif not validate_subject(msg[u'subject']) :
        return'invalid subject \n'
         
    if u'body' not in msg:
        return'no email body found\n'
   
        
#     return ('to' in msg and validate_email(msg['to'])
#             and 'to_name' in msg and validate_name(msg['to_name']) 
#             and 'from' in msg and validate_email(msg['from']) 
#             and 'from_name' in msg and validate_name(msg['from_name']) 
#             and 'subject' in msg and validate_subject(msg['subject'])
#             and 'body' in msg)
#     
   

def validate_email(value): 
    if type(value) is not unicode :
        return False
    if not all(c in printable for c in value) :
        return False
    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Za-z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Za-z]+)*$"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"$)',  # quoted-string
        re.UNICODE)
    domain_regex = re.compile(
        r'(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+(?:[A-Za-z]{2,6}|[A-Za-z0-9-]{2,}(?<!-))$',
        re.UNICODE)

    if u'@' not in value:
        return False

    user_part, domain_part = value.rsplit(u'@', 1)

    if not user_regex.match(user_part):
        return False
    if not domain_regex.match(domain_part) :
        return False

    return True


def validate_name(value):
    if type(value) is not unicode or len(value)==0:
        return False
    if not all(c in printable for c in value) :
        return False
    return True



def validate_subject(value):
    if type(value) is not unicode or len(value)==0:
        return False
    if not all(c in printable for c in value) :
        return False

    return True   


def validate_html(fragment_string):
    if type(fragment_string) is not unicode :
        return ('error', 'not unicode')
    ret = ('passed', None)
    try: 
        vld = HTMLValidator()
        vld.validate_fragment(html_template_head+fragment_string+html_template_tail)
        if (vld.errors) :
            ret = ('error', vld.errors)
        elif vld.warnings :
            ret = ('warning', vld.warnings)
           
    except Exception as e:
        ret =('unchecked', e)
    
    return ret
        
