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
import os,sys
from pysmssendmod.sites import *
homedir=os.environ["HOME"]
SHAREDIR="/usr/share/pysmssend/"
TEMPDIR="/.pysmssend/"
ACCOUNTS=homedir+TEMPDIR+"accounts/"
foobar=Browser()
foobar.set_handle_robots(False)

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
	testfoo=Browser()
	testfoo.set_handle_robots(False)
	# getting account name
	account=f.ui.comboBox.currentText()
	account=str.lower(str(account))
	#getting login credentials
	username=f.ui.lineEdit.text()
	password=f.ui.lineEdit2.text()
	# acc_openlogin is defined on sites modules
	login_page=acc_openlogin[str(account)]
	## insert headers  ##
	foobar.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]
	testfoo.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]
	try:
		if verbose:
			print("Contacting url --> "+login_page+"...")
		foobar.open(login_page)
	except:
		#this means that we couldnt connect to the site because of a network error
		print("ERROR: Please check your connection with your ISP...")
		errorlogin(f,account)
		tray.showlogin(account,0)
	
	## LOGIN SUCCESSED ##
	
	if account == "otenet":
		foobar.select_form(name="loginform") 
	else:
		foobar.select_form(nr=0)
	if account!="forthnet":
		foobar["username"] = username
		foobar["password"] = password
	else:#forthnet
		foobar["Username"] = username
		foobar["Password"] = password
	if verbose:
		print("Submitting your data...")
	foobar.submit()
	if verbose:
		print("Done")
	pass #create a small delay...
	if account=="otenet":
		acc_page="http://tools.otenet.gr/tools/tiles/Intro/generalIntro.do"
	else:
		acc_page = acc_opensms[str(account)]
	testfoo=foobar
	if verbose:
		print("Getting login feedback from --> "+acc_page+"...")
	foobar.open(acc_page)
	# Find out the remaining credits for our account
	error=0
	try:
		leftcred=creditsleft(f,account,testfoo,verbose)
		error=0;
	except:
		errorlogin(f,account)
		tray.showlogin(account,0)
		error=1;
	# Give feedback to user
	if error==0:# pass only if everything was ok
		f.ui.Result1.setText("Logged in to "+account+" ;-)")			
		tray.showlogin(account,1)
		# lock send and number field if we are short of credits
		myallowsend(f,leftcred,account)
		if f.ui.rememberMe.checkState()==2:#if Remember Me is ON
			if verbose:
				print("Saving account...")
			try:
			       file=open(homedir+TEMPDIR+account,"w")#open file according to account
			       file.write(username+"\n")#write username
			       file.write(password+"\n")#write password
			       file.close()#close it
			       if verbose:
			       		print("Account saved.. :-)")
			except:
				print("ERROR: Account was not stored!")
		else:#delte the file
			if os.path.exists(homedir+TEMPDIR+account):
				if verbose:
					print("Deleting your saved account...")
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
