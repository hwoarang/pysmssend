#!/usr/bin/env python
# -*- coding: utf-8 -*-
#***************************************************************************
#*    Pysmssend ( Source Code ) Login
#***************************************************************************
# This file is part of Pysmssend Project
#
#    Pysmssend Project is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 3 of the License, or
#     (at your option) any later version.
#
#    Pysmssend is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-
from pysmssendmod.input_validation import  *
from pysmssendmod.tray import *
from mechanize import Browser
from PyQt4 import QtCore
import os,sys,stat, time
import urllib2,urllib
from pysmssendmod.sites import *
from pysmssendmod.account_io import *

homedir=os.environ["HOME"]
SHAREDIR="/usr/share/pysmssend/"
TEMPDIR="/.pysmssend/"
ACCOUNTS=homedir+TEMPDIR+"accounts/"

## this function is called when login failed ##
def errorlogin(f,account):
        f.ui.Result1.setText("Login to "+account+" failed")
	f.ui.credits.clear()
	f.ui.lineEdit3.setReadOnly(True)
	f.ui.textEdit.setReadOnly(True)
	f.ui.lineEdit3.clear()
	f.ui.lineEdit3.insert("Error loggin in...:")
	f.ui.Send.setEnabled(False)
	f.ui.textEdit.setText("An error occurred while trying to login to "+account+".Either the username or password was wrong or there was a connectivity issue with the site. If you were trying to login to a Betamax account there might be a popup message for you waitting on your Betamax account. In any other case, if this problem persist please send a bug report at hwoarang@silverarrow.org")

#login function
def mylogin(f,tray,verbose,want_gpg,gpg_key):
	# getting account name
	account=f.ui.comboBox.currentText()
	account=str.lower(str(account))
	#getting login credentials
	username=f.ui.lineEdit.text()
	password=f.ui.lineEdit2.text()
	# Don't login if pennytel
	if account=="pennytel":
		from SOAPpy import WSDL
		import SOAPpy
		foobar=None	# Don't need browser for PennyTel

		WSDLFILE = 'http://pennytel.com/pennytelapi/services/PennyTelAPI?WSDL'
		_server = WSDL.Proxy(WSDLFILE)
		leftcred,blocked,currency,lastusage,others,zerobalancedate = _server.getAccount(username,password)
		if leftcred>0:
			error=0
			f.ui.Result1.clear()
			f.ui.credits.setText("Credit Left : "+currency+str(leftcred))
			f.ui.lineEdit_3.clear()
			f.ui.textEdit.clear()
			# Get Addressbook
			contacts = _server.getAddressBookEntries(username,password,"%")
			if contacts!=None:
				num_lines=len(contacts)
				f.ui.retranslateUi(f,num_lines)
				mycounter=0
				for contact in contacts:
					headerItem = QtGui.QTableWidgetItem()
					headerItem.setText(QtGui.QApplication.translate("self",str(mycounter+1), None, QtGui.QApplication.UnicodeUTF8))
					f.ui.tableWidget.setVerticalHeaderItem(mycounter,headerItem)
					
					name=contact.displayName
					item = QtGui.QTableWidgetItem()
					item.setText(QtGui.QApplication.translate("self", str(name), None, QtGui.QApplication.UnicodeUTF8))
					f.ui.tableWidget.setItem(mycounter,0,item)
					tel=contact.mobileNumber
					i=0
					flag=0
					item = QtGui.QTableWidgetItem()
					item.setText(QtGui.QApplication.translate("self", str(tel), None, QtGui.QApplication.UnicodeUTF8))
					f.ui.tableWidget.setItem(mycounter,1,item)
					mycounter=mycounter+1
				f.ui.Tabs.setCurrentIndex(0)
		else:
			error=1
	else:
		testfoo=Browser()
		testfoo.set_handle_robots(False)
		foobar=Browser()
		foobar.set_handle_robots(False)
		# acc_openlogin is defined on sites modules
		login_page=acc_openlogin[str(account)]
		## insert headers  ##
		foobar.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]
		testfoo.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]
		try:
			if verbose:
				print "Contacting url --> "+login_page+"..."
			foobar.open(login_page)
		except:
			#this means that we couldnt connect to the site because of a network error
			print "ERROR: Please check your connection with your ISP..."
			errorlogin(f,account)
			tray.showlogin(account,0)
		
		## LOGIN SUCCESSED ##
		
		if account == "otenet":
			foobar.select_form(name="loginform") 
		else:
			foobar.select_form(nr=0)
		if account == "voipbuster" or account == "lowratevoip":
			foobar["login[username]"] = username
			foobar["login[password]"] = password
		elif account != "forthnet":
			foobar["username"] = username
			foobar["password"] = password
		else:#forthnet
			foobar["Username"] = username
			foobar["Password"] = password
		if verbose:
			print "Submitting your data..."
		foobar.submit()
		if verbose:
			print "Done"
		pass #create a small delay...
		if account=="otenet":
			acc_page="http://tools.otenet.gr/tools/tiles/Intro/generalIntro.do"
		else:
			acc_page = acc_opensms[str(account)]
		testfoo=foobar
		if verbose:
			print "Getting login feedback from --> "+acc_page+"..."
		# Find out the remaining credits for our account
		error=0
		try:
			leftcred=creditsleft(f,account,testfoo,verbose)
			pass
			pass
			pass
			error=0
		except:
			errorlogin(f,account)
			tray.showlogin(account,0)
			error=1
	# Give feedback to user
	if error==0:# pass only if everything was ok
		f.ui.Result1.setText("Logged in to "+account+" ;-)")			
		tray.showlogin(account,1)
		# lock send and number field if we are short of credits
		myallowsend(f,leftcred,account)
		if f.ui.rememberMe.checkState()==2:#if Remember Me is ON
			if verbose:
				print "Saving account..."
			try:
			       file=open(homedir+TEMPDIR+account,"w")#open file according to account
			       file.write(username+"\n")#write username
			       file.write(password+"\n")#write password
			       file.close()#close it
			       if want_gpg:
				   		try:
							import gnupg
						except ImportError:
							print "I can't import the gnupg module"
							print "Make sure it's installed"
							sys.exit(1)
						gpg = gnupg.GPG()
						gpg.encoding = 'utf-8'
						try:
							with open(homedir+TEMPDIR+account) as afile:
								gpg.encrypt_file(afile,
											recipients=gpg_key,
											output=homedir+TEMPDIR+account+".enc")
								os.remove(homedir+TEMPDIR+account)
								account=account+".enc"
								os.chmod(homedir+TEMPDIR+account,stat.S_IRUSR|stat.S_IWUSR)
						except IOError as e:
							print e.strerror
			       if verbose:
			       		print "Account saved.. :-)"
			except:
				print "ERROR: Account was not stored!"
		else:#delte the file
			if os.path.exists(homedir+TEMPDIR+account):
				if verbose:
					print "Deleting your saved account..."
				os.remove(homedir+TEMPDIR+account)
		#display supported number format
		phonemessage=QtCore.QString("-- ")
		if account=="forthnet":
			phonemessage.append("694XXXXXXX")
		else:
			phonemessage.append("+30694XXXXXXX")
		phonemessage.append(" --")
		f.ui.lineEdit3.setText(phonemessage)
		return foobar,account,leftcred,username,password
	else:
		f.ui.Result1.setText("ERROR Logging in to "+account+" :-(")


def mysmssend(foobar,f,tray,account,verbose,leftcred,username,password):
	if account != "pennytel":
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
		elif account=="pennytel":
			from SOAPpy import WSDL                                                                                            
			import SOAPpy
			if verbose:
				print "Sending to " + number + "..."
			WSDLFILE = 'http://pennytel.com/pennytelapi/services/PennyTelAPI?WSDL'
			_server = WSDL.Proxy(WSDLFILE)
			sendTime=SOAPpy.dateTimeType((2000, 1, 1, 0, 0, 0, 4, 86, 0))
			results = _server.sendSMS(
			username,password,1,number,message,sendTime)
			sent=1
		else:# betamax
			#fixing the url
			url=acc_opensms2[str(account)]
			if verbose:
				print "Opening betamax sms url --> "+url
			#adding data
			values=[
				("username",username),
				("password",password),
				("to",number),
				("text",message)
			]
			data = urllib.urlencode(values)
			#adding header
			user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.162 Safari/535.19'
			headers = { 'User-Agent' : user_agent }
			#constructing the url
			req = urllib2.Request(url+data, headers=headers)
			response=urllib2.urlopen(req)
			time.sleep(4)
			report=response.read()
			sent=1
	except:
	       	f.ui.lineEdit_2.setText("Not sent ...")
		sent=0
        if sent==1:
		# get new credits lets
		if account!="forthnet" and account!="pennytel":
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
		if account=="pennytel":
			WSDLFILE = 'http://pennytel.com/pennytelapi/services/PennyTelAPI?WSDL'
			_server = WSDL.Proxy(WSDLFILE)
			leftcred,blocked,currency,lastusage,others,zerobalancedate = _server.getAccount(username,password)
			tray.showsentreport("Message was sent successfully ;-)",1)
			f.ui.Result1.clear()
			f.ui.credits.setText("Credit Left : "+str(leftcred))
			f.ui.lineEdit_3.clear()
			f.ui.textEdit.clear()
		elif account=="otenet" or account=="forthnet":
			if account=="otenet":
				username=f.ui.lineEdit.text()
				size2=145-len(username)
			else:#forthnet
				size2=160		
			if size<=size2:
				tray.showsentreport("Message was sent successfully ;-)",1)
				f.ui.Result1.clear()
				f.ui.credits.setText("SMS Left : "+str(cred))
				f.ui.lineEdit_3.clear()
				f.ui.textEdit.clear()
			elif size>size2:
				tray.showsentreport("Sorry I couldnt send the message :-( ",0)
		elif account!="otenet" and account!="forthnet": # in case we have betamax
			if size<=160:
				#now we need to open the response page in order to see if the message was send #succesfully
				result=report.find("<resultstring>")
				result2=report.find("</resultstring>")
				result3=report[result+14:result2]
				#do the final check
				#uff
				pass
				pass
				if verbose:
					print "Result: "+result3
				if result3=="success":
					tray.showsentreport("Message was sent successfully ;-)",1)
					f.ui.credits.setText("Credits Left: "+str(cred))
					f.ui.Result1.clear()
					f.ui.lineEdit_3.clear()
					f.ui.textEdit.clear()
				else:
					f.ui.lineEdit_2.setText(" Not sent ...")
					tray.showsentreport("Message didnt send",0)
			else:
				tray.showsentreport("Message too long...",0)
