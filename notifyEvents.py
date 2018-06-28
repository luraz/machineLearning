import ftplib, re, os, time, datetime, smtplib, socket
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

class NotifyEvents:
    def __init__(self, host=None, user=None, password=None, timeout=5):
        self.host = host if host else "ecstore01.am.local"
        self.user = user if user else "write"
        self.password = password if password else "write"
        self.timeout = timeout
        self.eventFolders = []
        self.filenames = []
        self.ftpConnection = None

        try:
            os.mkdir("serenity_events")
        except WindowsError:
            pass


    def sendMail(self):
        me = "ihagiu@bitdefender.com"
        you = "edragoslav@bitdefender.com"
        message = MIMEMultipart()
        message["Subject"] = ""
        message["From"] = "Ionut Nicolae HAGIU <ihagiu@bitdefender.com>"
        message["To"] = "edragoslav@bitdefender.com"
        text = ""
        mimeText = MIMEText(text, "plain")
        message.attach(mimeText)
        with open('andrei.pdf', 'rb') as fil:
            part = MIMEApplication(fil.read(), Name='elisei.pdf')
            part['Content-Disposition'] = 'attachment; filename="elisei.pdf"'
            message.attach(part)
        smtp = smtplib.SMTP(host="10.100.0.200", port=25)
        smtp.sendmail(me, you, message.as_string())
        smtp.quit()



    def close(self):
        if self.ftpConnection:
            self.ftpConnection.quit()
            self.ftpConnection = None


if __name__ == '__main__':
    notifyEvents = NotifyEvents()
    notifyEvents.sendMail()
    # notifyEvents.listEvents()
    # print notifyEvents.eventFolders
    #notifyEvents.syncAll(alarmMalwareDetect=True)
    #notifyEvents.close()
    