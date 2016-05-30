# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import make_msgid, formatdate

SSL = 'SSL'
TLS = 'StartTLS'

class EmailSender(object):
    def __init__(self, host, port=None, security=None, user=None, password=None):
        if port is None:
            if security == SSL:
                port = 465
            elif security == TLS:
                port = 587
            else:
                port = 25

        if security is SSL:
            self.connection = smtplib.SMTP_SSL(host, port)
        else:
            self.connection = smtplib.SMTP(host, port)
            if security is TLS:
                self.connection.starttls()
        if user and password:
            self.connection.login(user, password)

    def __del__(self):
        if self.connection:
            self.connection.quit()

    def send(self, sender, to, message):
        if isinstance(to, str):
            receivers = [to]
        elif to:
            receivers = list(to)
        else:
            receivers = []
        self.connection.sendmail(sender, receivers, message)

class Message(object):

    def __init__(self, subject='', body='', html='', nick_from=None, nick_to=None, encoding=None, attachments=None):
        self.subject = subject
        self.body = body
        self.html = html
        self.attachments = attachments or []
        self.encoding = encoding
        self.From = nick_from
        self.To = nick_to

    def __mime_message(self):
        encoding = self.encoding or 'utf-8'
        msg = MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = Header(self.From, encoding)
        msg['To'] = Header(self.To, encoding)
        msg['Date'] = formatdate()
        msg['Message-ID'] = make_msgid()

        if self.body and self.html:
            alternative = MIMEMultipart('alternative')
            alternative.attach(MIMEText(self.body, 'plain', encoding))
            alternative.attach(MIMEText(self.html, 'html', encoding))
            msg.attach(alternative)
        elif self.body:
            msg.attach(MIMEText(self.body, 'plain', encoding))
        elif self.html:
            msg.attach(MIMEText(self.html, 'html', encoding))

        for attachment in self.attachments:
            msg.attach(attachment)

        return msg

    def raw_message(self):
        return self.__mime_message().as_string()

    def __attach(self, filename, content, mimetype):
        maintype, subtype = mimetype.split('/', 1)

        if maintype == 'text':
            mime = MIMEText(content, subtype, None)
            mime.set_payload(content, utf8_charset)
        elif maintype == 'image':
            mime = MIMEImage(content, subtype)
        elif maintype == 'audio':
            mime = MIMEAudio(content, subtype)
        else:
            mime = MIMEBase(maintype, subtype)
            mime.set_payload(content)
            encoders.encode_base64(mime)

        self.__attach_mime(filename, mime)

    def __attach_mime(self, filename, mime):
        if not isinstance(mime, MIMEBase):
            raise TypeError('"mime" must be an instance of MIMEBase.')

        if filename:
            try:
                filename.encode('ascii')
            except UnicodeEncodeError:
                filename = ('utf-8', '', filename)

            mime.add_header('Content-Disposition', 'attachment', filename=filename)

        self.attachments.append(mime)

    def attach_file(self, path, mimetype=None):
        filename = os.path.basename(path)

        if not mimetype:
            mimetype, _ = mimetypes.guess_type(filename)

            if not mimetype:
                mimetype = DEFAULT_MIMETYPE

        maintype, subtype = mimetype.split('/', 1)
        readmode = 'r' if maintype == 'text' else 'rb'

        with open(path, readmode) as f:
            try:
                content = f.read()
            except UnicodeDecodeError:
                content = None

        if content is None:
            with open(path, 'rb') as f:
                content = f.read()
                mimetype = DEFAULT_MIMETYPE

        self.__attach(filename, content, mimetype)
