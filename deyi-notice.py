# -*- coding: utf-8 -*-

import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from pyquery import PyQuery as pq

from MiaoEmail import EmailSender, Message

def send_email(html, user, password):
    mail_host = 'smtp.qq.com'
    mail = EmailSender(mail_host, 465, 'SSL', user, password)

    sender = user
    receivers = user

    From = '发育不完善星人'
    To = "喵喵呜呜"
    subject = '一言不合就断水断电断气'
    body = '得意停水停电停气通知'
    message = Message(subject, body, html, From, To)

    mail.send(sender, receivers, message.raw_message())

def has_notice(notice, keyword):
    index = notice.find(keyword)
    if index is -1:
        return False
    else:
        return True

def main():
    try:
        keyword = sys.argv[1]
        print ('查询【%s】附近的水、电、气通知' % keyword)
        user = sys.argv[2] # QQ邮箱帐号
        password = sys.argv[3] # QQ邮箱密码
    except IndexError:
        print '请输入有效参数'
    else:
        doc = pq('http://api.deyi.com/frontpage/shownoti/')
        lis = doc('li')
        hit_lis = []

        for li in lis.items():
            notice = li.text().encode('utf-8')
            if has_notice(notice, keyword):
                hit_lis.append(li.html())
        if hit_lis:
            send_email('<br>'.join(hit_lis), user, password)

if __name__ == '__main__':
    main()
