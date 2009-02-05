#!/usr/bin/env python
# -*- coding: utf-8 -*-
#***************************************************************************
#*    Pysmssend  ( Source Code ) Cmdfunc
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
from mechanize import Browser 
from pysmssendmod.usage import *
from pysmssendmod.creditsleft import *
import sys
import urllib2,urllib
foobar = Browser()
foobar.set_handle_robots(False)
acc_openlogin = {
	'otenet':'http://tools.otenet.gr/tools/index.do'	
		}	
acc_opensms = {
	'otenet':'http://tools.otenet.gr/tools/tiles/web2sms.do?showPage=smsSend&mnu=smenu23',
	'voipbuster':'https://myaccount.voipbuster.com/clx/sendsms.php?',
	'voipdiscount':'https://myaccount.voipdiscount.com/clx/sendsms.php?',
	'lowratevoip':'https://myaccount.lowratevoip.com/clx/sendsms.php?',
	'voipbusterpro':'https://myaccount.voipbusterpro.com/clx/sendsms.php?',
	'freevoip':'https://myaccount.freevoip.com/clx/sendsms.php?',
	'12voip':'https://myaccount.12voip.com/clx/sendsms.php?',
	'webcalldirect':'https://myaccount.webcalldirect.com/clx/sendsms.php?',
	'nonoh':'https://myaccount.nonoh.com/clx/sendsms.php?',
	'justvoip':'https://myaccount.justvoip.com/clx/sendsms.php?'
	      }

def cmdlogin(account,username,password,verbose):#login function for cmd tools
	#Actually this code applies only to otenet logins.
	testfoo=Browser()
	testfoo.set_handle_robots(False)
	login_page=acc_openlogin[str(account)]#find url
	foobar.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]#add eaders
	testfoo.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]#add headers
	foobar.open(login_page)#open url
	foobar.select_form(name="loginform")
	foobar["username"] = username
        foobar["password"] = password
	foobar.submit()
	if verbose:
		print "Verifying data.."
	pass #create a small delay
	ok=0
	try:
		#Try to open sms page (this helps on deciding if login was correct )
		acc_page="http://tools.otenet.gr/tools/tiles/Intro/generalIntro.do"
		if verbose:
			print "Opening "+acc_page
		testfoo=foobar
		foobar.open(acc_page)#open sms page
		leftcred=creditsleft(account,testfoo)
		#if all the above worked then the login was ok (i hope so )
		test=foobar.geturl()
		if test==acc_page:
			if verbose:
				print "Logged in to "+account
				print "SMS Left: "+leftcred
		else: 
			print "Cannot login to "+account
	except:
		print "Cannot login to "+account
	
					

def sendsmscmd(account,username,password,number,message,verbose):
	acc_page = acc_opensms[str(account)]#find page
	foobar.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]
	testfoo=foobar
	if account=="otenet" or account=="yahoo":
		if verbose:
			print "Opening "+acc_page
		foobar.open(acc_page)
	if account=="otenet":
		try:
			foobar.select_form(name="sendform")
			
     		except:
        		sys.exit("Error contacting site... Please try again later\n")
	elif account=="voipbuster" or account=="voipdiscount" or account == "lowratevoip" or account=="voipbusterpro" or account=="freevoip" or account=="12voip" or account=="webcalldirect" or account=="nonoh" or account=="justvoip":
		#do nothing
		pass
		
	else:#if yahoo
		try:
			foobar.select_form(nr=0)  
		except:
			sys.exit("Error contacting site... Please try again later\n")
	if verbose:
		print "Creating message..."
	if account=="otenet":

		foobar["phone"] = number
       		foobar["message"] = message
	elif account=="yahoo":#this means yahoo
		foobar["ymsgSmsNumber"] = number
		foobar["ymsgSmsMessage"] = message
	try:
		if account=="otenet" or account=="yahoo":
			if verbose:
				print "Sending..."
         		foobar.submit()
			#work around for otenet report
			#find again the messages left and compare it with the initials
			# NOT TESTED
			leftcred2=creditsleft(account,testfoo)
			if leftcred==leftcred2:#if we have the same messages after the submit
			#it means that we didnt send the message
				#set final_report
				final_report=="failure"
			#hope it works
		else:
			#fixing the url
			url=acc_opensms[str(account)]
			if verbose:
				print "url: "+url
			#hack 1
			#adding data
			values={'username':username,
				'password':password,
				'from':username,
				'to':number,
				'text':message
				}
			if verbose:
				print "Verifying data"
			data = urllib.urlencode(values)
			#adding header
			user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
			headers = { 'User-Agent' : user_agent }
			#constructing the url
			if verbose:
				print "Sending..."
			req = urllib2.Request(url, data, headers)
			#small delay
			pass
			pass
			pass
			#its not my fault if betamax sends wrong reports
			response=urllib2.urlopen(req)
			report=response.read()
			#lets find out if the message was sent correctly
			data_response1=report.find("<resultstring>")
			data_response2=report.find("</resultstring>")
			final_report=report[data_response1+14:data_response2]
			#im done with the report.
	#finish the try except 
	except:
		sys.exit("Program terminated with error code")	
	#finisht the job
	#if verbose show the report and exit with error code if the report is failure
	if final_report=="failure":
		if verbose:
			print "Report: "+final_report
		sys.exit("Failed to send message")	
	else:
		if verbose:
			print "Report: "+final_report
		sys.exit(0)
