#!/usr/bin/env python2.4
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
import os,sys
homedir=os.environ["HOME"]
SHAREDIR="/usr/share/pysmssend/"
TEMPDIR="/.pysmssend/"
ACCOUNTS=homedir+TEMPDIR+"accounts/"
foobar=Browser()
foobar.set_handle_robots(False)
#these are the sites that im gonna open each time
acc_openlogin = {
	'otenet':'http://tools.otenet.gr/tools/index.do',
	'voipbuster':'https://myaccount.voipbuster.com/clx/index.php?part=plogin&username=Znexbf6430&password=',
	'voipdiscount':'https://myaccount.voipdiscount.com/clx/index.php?part=plogin&username=Znexbf6430&password=',
	'lowratevoip':'https://myaccount.lowratevoip.com/clx/index.php?part=plogin&username=Znexbf6430&password=',	
	'voipbusterpro':'https://myaccount.voipbusterpro.com/clx/index.php?part=plogin&username=Znexbf6430&password=',
	'freevoip':'https://myaccount.freevoip.com/clx/index.php?part=plogin&username=Znexbf6430&password=',
	'12voip':'https://myaccount.12voip.com/clx/index.php?part=plogin&username=Znexbf6430&password=',	
	'webcalldirect':'https://myaccount.webcalldirect.com/clx/index.php?part=plogin&username=Znexbf6430&password=',
	'nonoh':'https://myaccount.nonoh.net/clx/index.php?part=plogin&username=Znexbf6430&password=',
	'voipcheap':'https://myaccount.voipcheap.com/clx/index.php?part=plogin&username=Znexbf6430&password=',
	'justvoip':'https://myaccount.justvoip.com/clx/index.php?part=plogin&username=Znexbf6430&password='
	}	
acc_opensms = {
	'otenet':'http://tools.otenet.gr/tools/tiles/web2sms.do?showPage=smsSend&mnu=smenu23',
	'voipbuster':'https://myaccount.voipbuster.com/clx/index.php?part=menu&justloggedin=true',
	'voipdiscount':'https://myaccount.voipdiscount.com/clx/index.php?part=menu&justloggedin=true',
	'lowratevoip':'https://myaccount.lowratevoip.com/clx/index.php?part=menu&justloggedin=true',
	'voipbusterpro':'https://myaccount.voipbusterpro.com/clx/index.php?part=menu&justloggedin=true',
	'freevoip':'https://myaccount.freevoip.com/clx/index.php?part=menu&justloggedin=true',
	'12voip':'https://myaccount.12voip.com/clx/index.php?part=menu&justloggedin=true',
	'yahoo':'http://everywhere.yahoo.com/sms/sendsms',
	'webcalldirect':'https://myaccount.webcalldirect.com/clx/index.php?part=menu&justloggedin=true',
	'voipcheap':'https://myaccount.voipcheap.com/clx/index.php?part=menu&justloggedin=true',
	'nonoh':'https://myaccount.nonoh.net/clx/index.php?part=menu&justloggedin=true',
	'justvoip':'https://myaccount.justvoip.com/clx/index.php?part=menu&justloggedin=true'
	      }

#errorlogin function as imported from the obsolete errorlogin.py module
#this function is going to print some helping messages on the Gui. Not a big deal
def errorlogin(f,account):
        f.ui.Result1.setText("Login to "+account+" failed")
	f.ui.credits.clear()
	f.ui.lineEdit3.setReadOnly(True)
	f.ui.textEdit.setReadOnly(True)
	f.ui.lineEdit3.clear()
	f.ui.lineEdit3.insert("Error loggin in...:")
	f.ui.Send.setEnabled(False)
	f.ui.textEdit.setText("There was an error while trying to login on "+account+".Either the username or password was wrong or there was a connectivity issue with the site. If this error occured	when you tried to login with Betamax account it might be a popup message for you on your account informing you about previous credit transaction you might have with the company. If this problem persist please send a bug report at hwoarang_gr@users.sourceforge.net")

#login function
#im gonna be as "verbose" (lol) as possible
def mylogin(f,tray,verbose):
	testfoo=Browser()#here is our browser . neet :)
	testfoo.set_handle_robots(False)#this is hacking stuff. lol. We just ignore the robots.txt file
	account=f.ui.comboBox.currentText()#read account
	account=str.lower(str(account))#lower all the letter on the account
	#get data
	username=f.ui.lineEdit.text()#get the username from lineEdit field
	password=f.ui.lineEdit2.text()#get the password from lineEdit2 field
	# well if we DONT have yahoo account
	if account!="yahoo":
		login_page=acc_openlogin[str(account)]#find url
		foobar.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]#add eaders
		testfoo.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]#add headers
		try:
			if verbose:
				print "contacting url -> "+login_page+"...\n"
			foobar.open(login_page)#open url
		except:
			#this means that we couldnt connect to the site because of a network error
			print "contacting url failed... Please check your connection with your ISP...\n"
			errorlogin(f,account)
			#0 stands for failure
			tray.showlogin(account,0)
	#here is the good stuff
	#if we are using otenet 
	if account == "otenet":
		foobar.select_form(name="loginform")#select loginform 
	
	#this is in case we have betamax sites :)
	if account != "otenet" and account != "yahoo":
		foobar.select_form(nr=0)#form number=0. This means the first form
	if account=="otenet":
		foobar["username"] = username#parse the data
               	foobar["password"] = password#again
	if account != "otenet" and account != "yahoo":
		foobar["username"] = username#same as before
            	foobar["password"] = password#and again
	if account=="yahoo":
		pass#do nothing on yahoo
	if account!="yahoo":
		if verbose:
			print "submitting your data...\n"
		foobar.submit()#submit the stuff :)
		pass #create a small delay. Dont know why
		ok=0
		leftcread=0#we should initialize leftcread
		try:
			#Try to open sms page (this helps on deciding if login was correct )
			#and yes, i am ashamed of the way im trying to see if you are logged in
			#or not ,but it works ;)
			#so lets see if we can open the sms pages. If we can ,we can say we are logged in for sure
			if account=="otenet":
				acc_page="http://tools.otenet.gr/tools/tiles/Intro/generalIntro.do"
			else:
				acc_page = acc_opensms[str(account)]#find sms page
			testfoo=foobar
			if verbose:
				print "Opening sms page...\n"
			foobar.open(acc_page)#open sms page
			try:
				leftcred=creditsleft(f,account,testfoo,verbose)
				#if all the above worked then the login was ok (i hope so )
				ok=1
			except:
				sys.exit("couldnt open page")	
		except:
			errorlogin(f,account)
			tray.showlogin(account,0)		
		if ok==1:
			ok=0#reset the flag
			f.ui.Result1.setText("Logged in to "+account)			
			tray.showlogin(account,1)
			myallowsend(f,leftcred,account)
			homedir=os.environ["HOME"]
			if f.ui.rememberMe.checkState()==2:#if Remember Me is ON
				if verbose:
					print "Ah, i ve seen that you checked the Remember me button...\n"
					print "Im gonna save your data now...\n"
				try:
					#this is the same code as taken from mywritetofile.py module
				       file=open(homedir+TEMPDIR+account,"w")#open file according to account
				       file.write(username+"\n")#write username
				       file.write(password+"\n")#write password
				       file.close()#close it
				       if verbose:
				       		print "Account saved.. :) \n"
				except:
					print "Ah,Im sorry I couldnt save your data . My there is not enough space or what?\n"
			else:#delte the file
				if os.path.exists(homedir+TEMPDIR+account):
					if verbose:
						print "Deleting your saved account...\n"
					os.remove(homedir+TEMPDIR+account)
		elif ok==0:
			errorlogin(f,account)
			tray.showlogin(account,0)
	# i think its time to delete yahoo ?!
	else:#if its yahoo
		yahooinfo(tray)
	return foobar,account,leftcred,username,password
