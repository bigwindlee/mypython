#!/usr/bin/env python

import sys,smtplib,poplib
'''
comments
'''
SMTPserver = "smtp.163.com"
fromaddr = "bigwindlee@163.com"
toaddr = "bigwindlee@qq.com"

MsgHead = ['From:bigwindlee@163.com', 'To:bigwindlee@qq.com', 'Subject:powerful Python']
MsgBody = ['I am bigwind 2', 'This is my python program', 'my own client']
Msg = '\r\n\r\n'.join(['\r\n'.join(MsgHead), '\r\n'.join(MsgBody)])

s = smtplib.SMTP(SMTPserver)
s.set_debuglevel(1)
s.ehlo(SMTPserver)
#change the password
s.login("bigwindlee", "password")  
s.sendmail(fromaddr, toaddr, Msg)