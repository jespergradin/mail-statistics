import imaplib, email, time, sys
from dateutil import parser
from datetime import datetime, date

def getMailStatistics(name,server,user,password):
	mailserver = imaplib.IMAP4_SSL(server)
	mailserver.login(user, password.decode('base64'))
	mailserver.select("inbox")

	# get list of all (not deleted) mail
	result, data = mailserver.uid('search', None, 'NOT', 'DELETED')
	ids = data[0]
	id_list = ids.split()
	count = len(id_list)

	age = 0

	if count > 0:

		# get last mail
		last_email_uid = id_list[0]
		result, data = mailserver.uid('fetch', last_email_uid, '(RFC822)')
		raw_email = data[0][1]

		# get age of last mail
		email_message = email.message_from_string(raw_email)
		received = email_message['Received']
		dateReceived = received[received.find(';')+2:].strip()
		date = parser.parse(dateReceived)
		age = (datetime.now(date.tzinfo) - date).days

	return str(name) + ',' + str(count) + ',' + str(age)

output = str(datetime.now().date())

mailservers = (len(sys.argv) - 1) / 4
for i in range(0, mailservers):
	name = sys.argv[4*i+1]
	server = sys.argv[4*i+2]
	user = sys.argv[4*i+3]
	password = sys.argv[4*i+4]
	output += ',' + getMailStatistics(name, server, user, password)

print output
