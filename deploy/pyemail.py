# -*- coding: utf-8 -*-
"""
===============================================================================
=============================== PYTHON EMAIL API ==============================
===============================================================================
@author: QUAN YUAN
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# Send attached file with email
class Emailsender:
    def __init__(self, sender, password, receiver):
        
        # the email address of the sender: string
        self.sender = sender
        # the email password of the sender: string
        self.password = password
        # the email address of the recipient: string
        self.receiver = receiver
        
    def email_file(self, title, efile, efile_name, emsg = '', smtp_address = 'smtp.163.com'):
        # the email title: string
        # the efile: file_name list
        
        # define the subject of the email
        message = MIMEMultipart()
        message['From'] = "{}".format(self.sender)
        message['To'] = ",".join(self.receiver)
        message['Subject'] = Header(title, 'utf-8')
        
        # define the message
        message.attach(MIMEText(emsg, 'plain', 'utf-8'))
        
        # attachment
        for each_attach, each_attach_name in zip(efile, efile_name):
            att = MIMEText(open(each_attach, 'rb').read(), 'base64', 'utf-8')
            att['Content-Type'] = 'application/octet-stream'
            att['Content-Disposition'] = "attachment; filename = " + each_attach_name
            message.attach(att)
        
        # send the email
        try:
            smtp = smtplib.SMTP()
            smtp.connect(smtp_address)
            smtp.login(self.sender, self.password)
            smtp.sendmail(self.sender, self.receiver, message.as_string())
            smtp.quit()
            print "EMAIL SUCCESS"
        except:
            print "EMAIL ERROR"
        
    def email_msg(self, title, emsg, smtp_address = 'smtp.163.com'):
        # the email title: string
        # the emsg: string
        
        # define the subject of the email
        message = MIMEMultipart()
        message['From'] = "{}".format(self.sender)
        message['To'] = ",".join(self.receiver)
        message['Subject'] = Header(title, 'utf-8')
        
        # define the message
        message.attach(MIMEText(emsg, 'plain', 'utf-8'))
        
        # send the email
        try:
            smtp = smtplib.SMTP()
            smtp.connect(smtp_address)
            smtp.login(self.sender, self.password)
            smtp.sendmail(self.sender, self.receiver, message.as_string())
            smtp.quit()
            print "EMAIL SUCCESS"
        except:
            print "EMAIL ERROR"
        