from pysmssendmod.tray import *
from mechanize import Browser
from pysmssendmod.creditsleft import *
import sys
import urllib2,urllib
import os,time
from pysmssendmod.sites import *


def mysmssend(foobar,f,trayic,account,verbose,leftcred,username,password):
	acc_page = acc_opensms[str(account)]#find page
	foobar.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]
	testfoo=foobar
	if account=="otenet" or account=="forthnet":
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
	elif account=="forthnet":
		try:
			foobar.select_form(nr=0)
		except:
			sys.exit("Error contacting site... Please try again later\n")
	# passing data
	if account=="otenet":
		foobar["phone"] = number
	        foobar["message"] = message
	elif account=="forthnet":
		foobar["txtTo"] = number
		foobar["txtMessage"] = message

	# convert message to plain text. It is easier to handle it
	message=f.ui.textEdit.toPlainText()
	size=message.length()
	try:
		if account=="otenet" or account=="forthnet":
			if verbose:
				print "Sending..."
         		foobar.submit()
			sent=1
		else:# betamax
			#fixing the url
			url=acc_opensms[str(account)]
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
		if account=="otenet":
			cred=creditsleft(f,account,testfoo,verbose)
		elif account=="forthnet":
			gethtml=foobar.response()
			html=gethtml.read()
			balance=html.find("<span id=\"lbPerDay\">")
			balanceline=html[balance:]
			temp1=balanceline.split("<span id=\"lbPerDay\">")
			temp2=temp1[1].split("</span>")
			temp3=temp2[0].split("/");
		        cred=str(5-int(temp3[0]))
		if account=="otenet" or account=="forthnet":
			if account=="otenet":
				username=f.ui.lineEdit.text()
				size2=145-len(username)
			else:#forthnet
				size2=160		
			if size<=size2:
				tray.showsentreport("Message was sent successfully ;-)")
				f.ui.Result1.clear()
				f.ui.credits.setText("SMS Left : "+str(cred))
				f.ui.lineEdit_3.clear()
				f.ui.textEdit.clear()
			elif size>size2:
				tray.showsentreport("Sorry I couldnt send the message :-( ")
		elif account!="otenet" and account!="forthnet": # in case we have betamax
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
				else:
					f.ui.lineEdit_2.setText(" Not sent ...")
					tray.showsentreport("Message didnt send")
			else:
				tray.showsentreport("Message too long...")
