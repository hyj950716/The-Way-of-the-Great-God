import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr


def send_mail():
    """发送邮件"""
    mail_host = "smtp.126.com"  # 设置服务器
    mail_user = "huxiaofang950716"  # 用户名
    mail_pass = "QHRFGFXWKPFXSJNA"  # 口令,SMTP开启后的授权码
    sender = 'huxiaofang950716@126.com'  # 发件人地址
    receivers = ['745587545@qq.com', "jiang.qiufei@fonixtree.com","huxiaofang950716@163.com"]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = formataddr(["胡英俊", "huxiaofang950716@126.com"])
    message['To'] = ','.join(receivers)
    subject = '接口自动化测试执行报告'  # 发送邮件的标题
    message['Subject'] = Header(subject, 'utf-8')  # 设定邮件的标题
    message["Accept-Language"] = "zh-CN"  # 设定邮件的语言
    message["Accept-Charset"] = "ISO-8859-1,utf-8,gbk"  # 设定邮件的编码
    # 邮件正文内容
    message.attach(MIMEText('最新执行的接口自动化测试报告，请参阅附件内容！', 'plain', 'utf-8'))

    # 构造附件1
    att = MIMEBase('application', 'octet-stream')
    att.set_payload(open("接口测试报告.html", 'rb').read())  # 接口测试报告.html:上传附件的相对路径地址
    att.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', "接口测试报告.html"))  # 设定邮件发送时候的邮件名称
    encoders.encode_base64(att)
    message.attach(att)

    try:
        smtpObj = smtplib.SMTP(mail_host)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)


if __name__ == "__main__":
    send_mail()
