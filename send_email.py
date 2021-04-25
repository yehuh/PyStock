import smtplib
from email.mime.multipart import MIMEMultipart #email內容載體
from email.mime.text import MIMEText #用於製作文字內文
from email.mime.base import MIMEBase #用於承載附檔
from email import encoders #用於附檔編碼
import datetime
import ssl


# 預設本周要寄出上周一至周日的報告，故抓出上周一的日期
today_date = datetime.date.today()
days_to_mon = today_date.weekday()

this_mon = today_date - datetime.timedelta(days = days_to_mon)
last_mon = this_mon - datetime.timedelta(days = 7)

#寄件者使用的Gmail帳戶資訊
gmail_user = 'yehuhuh@gmail.com'
gmail_password = 'dkx6irsw'
from_address = gmail_user




to_address = ['yeh_uh@yahoo.com.tw']  
Subject = "Here is the Weekly Report ({})".format(last_mon)
contents = """
Hi my friend,
Attached please find the Weekly Play Report ({}) you requested.

Feel free to reach me if you guys have any suggestion.

Regards,
Angela
""".format(last_mon)

#開始組合信件內容
mail = MIMEMultipart()
mail['From'] = from_address
mail['To'] = ', '.join(to_address)
mail['Subject'] = Subject
#將信件內文加到email中
mail.attach(MIMEText(contents))


# 設定smtp伺服器並寄發信件    
smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
smtpserver.ehlo()
smtpserver.login(gmail_user, gmail_password)
smtpserver.sendmail(from_address, to_address, mail.as_string())
smtpserver.quit()
