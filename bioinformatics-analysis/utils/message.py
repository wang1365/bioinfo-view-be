import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings


def send_email(subject, content, to_addr, attach=None):
    message = MIMEMultipart()
    text = MIMEText(content, "html", "utf-8")
    if attach:
        for attach_obj in pack_email_files(attach):
            message.attach(attach_obj)
    message['Subject'] = subject  # 邮件标题
    message['To'] = to_addr  # 收件人
    message['From'] = settings.EMAIL_SENDER  # 发件人
    message.attach(text)
    smtp = smtplib.SMTP_SSL(
        settings.EMAIL_HOST,
        settings.EMAIL_PORT)  # 实例化smtp服务器
    smtp.login(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)  # 发件人登录
    smtp.sendmail(
        settings.EMAIL_SENDER,
        [to_addr],
        message.as_string())  # as_string 对 message 的消息进行了封装
    smtp.close()


def pack_email_files(attach={}):
    attach_objs = []
    for _type, file_list in attach.items():
        if _type == "image":
            for file in file_list:
                imagepart = MIMEImage(
                    open(file, 'rb').read(), file.split('.')[-1])
                imagepart.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=os.path.basename(file))
                attach_objs.append(imagepart)
        elif _type == "file":
            for file in file_list:
                filepart = MIMEApplication(open(file, 'rb').read())
                filepart.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=os.path.basename(file))
                attach_objs.append(filepart)
    return attach_objs
