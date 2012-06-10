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
from pysmssendmod.creditsleft import *
from pysmssendmod.myallowsend import  *
from pysmssendmod.tray import *
from mechanize import Browser
from PyQt4 import QtCore
import os,sys,stat
from pysmssendmod.sites import *
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
def mylogin(f,tray,verbose):
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
		if account == "voipbuster":
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
			       os.chmod(homedir+TEMPDIR+account,stat.S_IRUSR|stat.S_IWUSR)
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
