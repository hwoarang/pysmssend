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
import sys
import urllib2,urllib
foobar = Browser()
foobar.set_handle_robots(False)

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

acc_verify = {
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

acc_opensms = {
	'otenet':'http://tools.otenet.gr/tools/tiles/web2sms.do?showPage=smsSend&mnu=smenu23',
	'voipbuster':'https://myaccount.voipbuster.com/clx/sendsms.php?',
	'voipdiscount':'https://myaccount.voipdiscount.com/clx/sendsms.php?',
	'lowratevoip':'https://myaccount.lowratevoip.com/clx/sendsms.php?',
	'voipbusterpro':'https://myaccount.voipbusterpro.com/clx/sendsms.php?',
	'freevoip':'https://myaccount.freevoip.com/clx/sendsms.php?',
	'12voip':'https://myaccount.12voip.com/clx/sendsms.php?',
	'webcalldirect':'https://myaccount.webcalldirect.com/clx/sendsms.php?',
	'voipcheap':'https://myaccount.voipcheap.com/clx/sendsms.php?',
	'nonoh':'https://myaccount.nonoh.com/clx/sendsms.php?',
	'justvoip':'https://myaccount.justvoip.com/clx/sendsms.php?'
	      }

##################### CREDITS LEFT ###############################
def creditsleft(account,foobar,verbose):
	if account != "otenet" and account != "yahoo":
		if verbose:
			print "Trying to find how much money left ...\n"
		gethtml=foobar.response()#get the html and parse it. Im not going to tell the details. tt us pure python
		html=gethtml.read()
		balance=html.find("balanceid")
		balanceline=html[balance:]
		euros=balanceline.split('&nbsp;')
		creditsleft=euros[1].split('</b>')
		final=creditsleft[0]
		print "Credits Left : "+str(final)
	elif account=="otenet":
		foobar.open("http://tools.otenet.gr/tools/tiles/Intro/generalIntro.do")
		gethtml=foobar.response()
		html=gethtml.read()
		balance=html.find("""  <a href="/tools/tiles/web2sms.do?showPage=smsSend&amp;mnu=smenu23"> <span class="txtmov10b_yellow">""")
		balanceline=html[balance:]
		data=balanceline.split()
		dataline=data[3]
		temp1=dataline.split("""class="txtmov10b_yellow">""")
		temp2=temp1[1]
		left=temp2.split("</span>")
		final=left[0]
		print "SMS Left : "+str(final)
	else:#this means yahoo
		print "Unlimited"
	#final is the amount of money we have :)		
	return final
#############################################################################


##################### CMD LOGIN ############################################
def cmdlogin(account,username,password,verbose):#login function for cmd tools
	#Actually this code applies only to otenet logins.
	testfoo=Browser()
	testfoo.set_handle_robots(False)
	login_page=acc_openlogin[str(account)]#find url
	foobar.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]#add eaders
	testfoo.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]#add headers
	foobar.open(login_page)#open url
	if account=="otenet":
		foobar.select_form(name="loginform")
	elif account!="otenet" and account!="yahoo":
		foobar.select_form(nr=0)
	foobar["username"] = username
        foobar["password"] = password
	foobar.submit()
	if verbose:
		print "Verifying data.."
	pass #create a small delay
	ok=0
	testfoo=foobar
	try:
		leftcred=creditsleft(account,testfoo,verbose)
	except:
		sys.exit("Cannot login to "+account)
	if verbose:
		print "Logged in to "+account
		if account=="otenet":
			print "SMS left: "+leftcred
		elif account=="otenet" and account!="yahoo":
			print "Credits left: "+leftcred


def sendsmscmd(account,username,password,number,message,verbose):
	acc_page = acc_opensms[str(account)]#find page
	foobar.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]
	testfoo=foobar
	foobar.open(acc_page)
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
	if verbose:
		print "Creating message..."
	if account=="otenet":
		foobar["phone"] = number
       		foobar["message"] = message
	elif account=="yahoo":#this means yahoo
		foobar["ymsgSmsNumber"] = number
		foobar["ymsgSmsMessage"] = message
	else:
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
	try:
		if account=="otenet" or account=="yahoo":
			if verbose:
				print "Sending..."
			foobar.submit()
			leftcred2=creditsleft(account,testfoo,verbose)
			if leftcred==leftcred2:#if we have the same messages after the submit
				#it means that we didnt send the message
				#set final_report
				final_report=="failure"
				#hope it works
        	else:
			if verbose:
				print "Sending..."
			req = urllib2.Request(acc_opensms[str(account)], data, headers)
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
