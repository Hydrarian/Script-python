import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
mail_content = '''Test invio mail'''
#The mail addresses and password
sender_address = 'berardi.bot@gmail.com'
sender_pass = 'te312502'
receiver_addresses = ['j.venditti@gberardi.com', 'm.tommolini@gberardi.com', 'm.buldrini@gberardi.com']

def sendmail(receiver_address):
	#Setup the MIME
	message = MIMEMultipart()
	message['From'] = sender_address
	message['To'] = receiver_address
	message['Subject'] = 'Test email'
	#The subject line
	#The body and the attachments for the mail
	message.attach(MIMEText(mail_content, 'plain'))
	attach_file_name = 'C:\\Users\\tommolini\\Desktop\\a.txt'
	attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
	payload = MIMEBase('application', 'octate-stream')
	payload.set_payload((attach_file).read())
	encoders.encode_base64(payload) #encode the attachment
	#add payload header with filename
	payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
	message.attach(payload)
	#Create SMTP session for sending the mail
	session = smtplib.SMTP('smtp.gmail.com:587') #use gmail with port
	session.ehlo()
	session.starttls() #enable security
	session.login(sender_address, sender_pass) #login with mail_id and password
	text = message.as_string()

	session.sendmail(sender_address, receiver_address, text)
	session.quit()
	print('Mail mandata')

for i in receiver_addresses:
	sendmail(i)