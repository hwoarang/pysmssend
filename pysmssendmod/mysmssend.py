from pysmssendmod.tray import *
from mechanize import Browser
from pysmssendmod.creditsleft import *
import sys
import urllib2,urllib
import os,time
# due to upstream changes , we need to introduce ( again *sigh* ) the old way for sending messages
acc_opensms = {
	'otenet':'http://tools.otenet.gr/tools/tiles/web2sms.do?showPage=smsSend&mnu=smenu23',
	'voipbuster':'https://myaccount.voipbuster.com/clx/sendsms.php?username=',
	'voipdiscount':'https://myaccount.voipdiscount.com/clx/sendsms.php?username=',
	'lowratevoip':'https://myaccount.lowratevoip.com/clx/sendsms.php?username=',
	'voipbusterpro':'https://myaccount.voipbusterpro.com/clx/sendsms.php?username=',
	'freevoip':'https://myaccount.freevoip.com/clx/sendsms.php?username=',
	'12voip':'https://myaccount.12voip.com/clx/sendsms.php?username=',
	'webcalldirect':'https://myaccount.webcalldirect.com/clx/sendsms.php?username=',
	'nonoh':'https://myaccount.nonoh.com/clx/sendsms.php?username=',
	'justvoip':'https://myaccount.justvoip.com/clx/sendsms.php?username',
	'voipcheap':'https://myaccount.voipcheap.com/clx/sendsms.php?username'
	      }
def mysmssend(foobar,f,trayic,account,verbose,leftcred,username,password):
	#code is like shit. Sorry about that
	if account!="NULL":
		acc_page = acc_opensms[str(account)]#find page
	else:
		#find the account by reading the combo again :(
		account=f.ui.comboBox.currentText()#read account
		account=str.lower(str(account))
	foobar.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]
	testfoo=foobar
	if account=="otenet" or account=="yahoo":
		foobar.open(acc_page)
	#get message and phone and username and password
	username=f.ui.lineEdit.text()
        password=f.ui.lineEdit2.text()
	number=f.ui.lineEdit3.text()
        message2=f.ui.textEdit.toPlainText()
	#convert Qstring to utf8
	message=message2.toUtf8()
	if account=="otenet":
		try:
			foobar.select_form(name="sendform")

     		except:
        		sys.exit("Error contacting site... Please try again later\n")
	elif account!="otenet" and account!="yahoo":
		#do nothing
		pass

	else:#if yahoo
		try:
			foobar.select_form(nr=0)
		except:
			sys.exit("Error contacting site... Please try again later\n")

	# passing data
	if account=="otenet":
		foobar["phone"] = number
	        foobar["message"] = message
	elif account=="yahoo":#this means yahoo
		foobar["ymsgSmsNumber"] = number
		foobar["ymsgSmsMessage"] = message

	message=f.ui.textEdit.toPlainText()
	size=message.length()
	try:
		if account=="otenet" or account=="yahoo":
         		foobar.submit()
			sent=1
		else:
			#fixing the url
			url=acc_opensms[str(account)]
			#hack 1
			#adding data
			values={'username':username,
				'password':password,
				'from':username,
				'to':number,
				'text':message
				}
			data = urllib.urlencode(values)
			#adding header
			user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
			headers = { 'User-Agent' : user_agent }
			#constructing the url
			req = urllib2.Request(url, data, headers)
			response=urllib2.urlopen(req)
			#create a 4 seconds delay. If you are using adsl you want have any problems
			#for those people who use dial up im sorry :P
			#this delay is to allo urllib2 to give us a proper report of sms
			time.sleep(4)
			#im doing this because urllib is kinda stupid and returns false response if i dont add a small delay
			#duh
			report=response.read()
			sent=1
	except:
	       	f.ui.lineEdit_2.setText("Not sent ...")
		sent=0
        if sent==1:
		# get new credits lets
		cred=creditsleft(f,account,testfoo,verbose)
		if account=="otenet":
			username=f.ui.lineEdit.text()
			size2=145-len(username)
			if size<=size2:
				tray.showsentreport("Message was sent successfully ;-)")
				f.ui.Result1.clear()
				f.ui.credits.setText("SMS Left : "+str(cred))
				f.ui.lineEdit_3.clear()
				f.ui.textEdit.clear()
			elif size>size2:
				tray.showsentreport("Sorry I couldnt send the message :-( ")
		elif account!="otenet" and account!="yahoo": # in case we have betamax
			if size<=160:
				#now we need to open the response page in order to see if the message was send #succesfully
				result=report.find("<resultstring>")
				result2=report.find("</resultstring>")
				result3=report[result+14:result2]
				#do the final check
				#uff
				print result3
				if result3=="success":
					tray.showsentreport("Message was sent successfully ;-)")
					f.ui.credits.setText("Credits Left: "+str(cred))
					f.ui.Result1.clear()
					f.ui.lineEdit_3.clear()
					f.ui.textEdit.clear()
					#save data to file ;)
					print "Saving account information..."
					homedir=os.environ["HOME"]
					if f.ui.rememberMe.checkState()==2:#if Remember Me is ON
						mywritetofile(account,username,password)#write to file
				else:
					f.ui.lineEdit_2.setText(" Not sent ...")
					showsentreport2(trayic)
			else:
				tray.showsentreport("Sorry, I couldnt send the message :-(")
		else:#this is for yahoo messaging
			if size<=120:
				f.ui.lineEdit_2.setText("Message Sent")
				showsentreport1(trayic)
				f.ui.Result1.clear()
				f.ui.lineEdit_3.clear()
				f.ui.textEdit.clear()
