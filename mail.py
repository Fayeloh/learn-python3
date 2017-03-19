#-----------------------------------------------------------电子邮件
#MUA,MTA,MDA
#-----------------------------------------------------------SMTP
#邮件分三种：纯文本、HTML邮件、带附件邮件
#纯文本邮件

from email.mime.text import MIMEText
msg = MIMEText('hello,smtp....','plain','utf-8')			#第一个参数是邮件正文，第二个参数是MIME的subtype，plain表示纯文本

#输入Email口令
from_addr = input('From:')
password = input('Password:')
#输入收件人地址
to_addr = input('To:')
#输入SMTP服务器地址
smtp_server = input('SMTP server:')

import smtplib
server = smtplib.SMTP(smtp_server,25)		#smtp的默认端口号25
server.set_debuglevel(1)					#set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息
server.login(from_addr,password)

server.sendmail(from_addr,[to_addr],msg.as_string())	#可以传送多人，所以用list。将MIMEText转换为str
server.quit()
#报错：因为使用QQ邮箱发邮件的，所以先把smtplib.SMTP()改成smtplib.SMTP_SSL(),然后将smtp的端口号25改为465

##-----------------------------------------------------------发送附件
##-----------------------------------------------------------发送图片
##-----------------------------------------------------------同时支持HTML和
##-----------------------------------------------------------加密SMTP


#-----------------------------------------------------------POP3
#收邮件分两步：1.用popliv把邮件的原始文本下载到本地
#			  2.用email解析原始文本，还原为邮箱对象

##-----------------------------------------------------------通过pop3下载邮件
##----------------------------------------------------------——解析邮件




#关于邮箱这辣眼睛的问题，等到以后慢慢查找原因吧