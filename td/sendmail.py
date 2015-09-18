# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 13:43:01 2015

@author: guosen
"""

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


class sendmail(object):
    def __init__(self, smtp_server, from_addr, password):
        self.__smtp_server = smtp_server        
        self.__from_addr = from_addr
        self.__password = password
        
    def send(self, content, to_addr):
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = self.__from_addr
        msg['To'] = ', '.join(to_addr)
        msg['Subject'] = Header(u'来自TD的提醒……', 'utf-8').encode()
        
        server = smtplib.SMTP(self.__smtp_server, 25)
        server.set_debuglevel(1)
        server.login(self.__from_addr, self.__password)
        server.sendmail(self.__from_addr, to_addr, msg.as_string())
        server.quit()