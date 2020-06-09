# import all the necessary modules
import smtplib

#init SMS and email client
server = smtplib.SMTP('smtp.tinu.tech', 587)
server.ehlo()
server.starttls()
server.login("homework.manager@tinu.tech", "lICLEH(7")

msg = "Test Email from the Homework Manager"
server.sendmail("homework.manager@tinu.tech", "tinuvanapamula@gmail.com", "\r\n".join(["From: homework.manager@tinu.tech","To: tinuvanapamula@gmail.com","Subject: Test Email","",msg]))
server.quit()
