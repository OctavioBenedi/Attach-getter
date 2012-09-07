import poplib
import email
import mimetypes
import os
# Import the email modules we'll need
from email.parser import Parser

mimes = ["text/plain","image/tiff","images/x-tif","image/x-tiff",
"application/tif","application/tiff","application/x-tif",
"application/x-tiff"]

def WriteAttachment(msg):
	counter = 1
	directory = "/tmp"
	for part in msg.walk():
		# multipart/* are just containers
		if part.get_content_maintype() == 'multipart':
			continue
		# Applications should really sanitize the given filename so that an
		# email message can't be used to overwrite important files
		filename = part.get_filename()
		if not filename:			
			ext = mimetypes.guess_extension(part.get_content_type())
			if not ext:
				# Use a generic bag-of-bits extension
				ext = '.bin'
			filename = 'part-%03d%s' % (counter, ext)
		basefileName, basefileExtension = os.path.splitext(filename)
		if basefileExtension != ".txt":
			continue
		counter += 1
		print "Saving file: "+os.path.join(directory, filename)
		fp = open(os.path.join(directory, filename), 'wb')
		fp.write(part.get_payload(decode=True))
		fp.write('\n');
		fp.close()


account_user = 'username_on_server' 
account_password = 'pop3_password'
allowed_sender_address = "a_mail_address_to_receive_from"
Mailbox = poplib.POP3_SSL('pop.googlemail.com', '995') 
Mailbox.user(account_user) 
Mailbox.pass_(account_password) 

numMessages = len(Mailbox.list()[1])

if (numMessages):
	print ("Found %d new messages\n" % numMessages)
	for i in range(numMessages):
		response, msg_as_list, size = Mailbox.retr(i+1)
		headers = Parser().parsestr('\r\n'.join(msg_as_list))
		print('From: %s' % headers['from'])
		print('Subject: %s' % headers['subject'])		
		name, address = email.utils.parseaddr('From: %s' % headers['from'])
		if address == allowed_sender_address:			
			msg = email.message_from_string('\r\n'.join(msg_as_list))
			WriteAttachment(msg)
		print '\n'

Mailbox.quit()

