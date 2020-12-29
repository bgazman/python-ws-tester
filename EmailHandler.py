import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import Config


# def send_mail(send_from, send_to, subject, text, files=None,
#               server="127.0.0.1"):
#     assert isinstance(send_to, list)
#
#     msg = MIMEMultipart()
#     msg['From'] = send_from
#     msg['To'] = COMMASPACE.join(send_to)
#     msg['Date'] = formatdate(localtime=True)
#     msg['Subject'] = subject
#
#     msg.attach(MIMEText(text))
#
#     for f in files or []:
#         with open(f, "rb") as fil:
#             part = MIMEApplication(
#                 fil.read(),
#                 Name=basename(f)
#             )
#             part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
#             msg.attach(part)
#
#
#     smtp = smtplib.SMTP(server)
#     smtp.sendmail(send_from, send_to, msg.as_string())
#     smtp.close()
def sendEmail(buildNum):
    msg = MIMEMultipart()
    msg['From'] = Config.mailFrom
    msg['To'] = ', '.join(Config.mailTo)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Test Jenkins python invocation"
    msg['CC'] = ', '.join(Config.mailCC)
    text = "Jenkins Invoked build test for Build Number :  " + buildNum
    msg.attach(MIMEText(text))
    filename = Config.app_home + '/Reports/' +buildNum + ".html"
    f = file(filename)
    attachment = MIMEText(f.read())
    attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(attachment)
    smtp = smtplib.SMTP(Config.mailServer)
    smtp.sendmail(Config.mailFrom, Config.mailTo + Config.mailCC, msg.as_string())
    smtp.close()
