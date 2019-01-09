#_*_coding:utf-8_*_

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders
import time
from interface_project.library import scripts
from interface_project.globalVar import gl

import yaml,os,base64


class EmailClass(object):
    def __init__(self):
        self.curDateTime = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())) #当前日期时间
        self.config = scripts.getYamlfield(os.path.join(gl.configPath,'config.yaml')) #配置文件路径
        self.sender = self.config['EMAIL']['Smtp_Sender'] # 从配置文件获取，发件人
        self.receivers = self.config['EMAIL']['Receivers']  # 从配置文件获取，接收人
        self.msg_title = self.config['EMAIL']['Msg_Title'] #从配置文件获取，邮件标题
        self.sender_server = self.config['EMAIL']['Smtp_Server'] #从配置文件获取，发送服务器
        self.From = self.config['EMAIL']['From']
        self.To = self.config['EMAIL']['To']

    '''
    配置邮件内容
    '''
    @property
    def setMailContent(self):
        print self.receivers
        msg = MIMEMultipart()
        msg['From'] = Header(self.From,'utf-8')
        msg['To'] = self.To
        msg['Subject'] = Header('%s%s'%(self.msg_title,self.curDateTime),'utf-8')

        #两个附件路径
        reportfile = os.path.join(gl.reportPath, 'Report.html')
        countPath = os.path.join(gl.reportPath,'count.xlsx')

        #增加邮件内容为html
        fp = open(reportfile, 'rb')
        reportHtmlText = fp.read()
        msg.attach(MIMEText(reportHtmlText,'html','utf-8'))
        fp.close()

        #增加附件
        html = self.addAttach(reportfile,filename='Report%s.html'%self.curDateTime) #自动化测试报告附件
        xlsx = self.addAttach(countPath,filename='接口开发情况统计表.xlsx') #xlsx接口进度表
        msg.attach(html)
        msg.attach(xlsx)

        return msg


    '''
    增加附件
    '''
    def addAttach(self,apath,filename='Report.html'):
        with open(apath, 'rb') as fp:
            attach = MIMEBase('application','octet-stream')
            attach.set_payload(fp.read())
            attach.add_header('Content-Disposition', 'attachment', filename=filename)
            encoders.encode_base64(attach)
            fp.close()
            return attach


    '''
    发送电子邮件
    '''
    def sendEmail(self,message):
        try:
            try: #防止25端口被封,比如阿里云
                smtpObj = smtplib.SMTP()
                smtpObj.connect(self.sender_server,25)
            except:
                smtpObj = smtplib.SMTP_SSL(self.sender_server,465)
                smtpObj.connect(self.sender_server)

            smtpObj.login(self.sender,self.config['EMAIL']['Password'])
            smtpObj.sendmail(self.sender,self.receivers , message.as_string())
            smtpObj.quit()
            print "邮件发送成功"
        except smtplib.SMTPException as ex:
            print "Error: 无法发送邮件.%s"%ex

    #发送调用
    @property
    def send(self):
        self.sendEmail(self.setMailContent)

if __name__=="__main__":
    EmailClass().send

