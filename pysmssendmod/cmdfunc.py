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
from pysmssendmod.sites import *
import sys
import urllib2,urllib
foobar = Browser()
foobar.set_handle_robots(False)


##################### CREDITS LEFT ###############################
def creditsleft(account,foobar):
	if account != "otenet" and account != "forthnet":
		gethtml=foobar.response()#get the html and parse it. Im not going to tell the details. tt us pure python
		html=gethtml.read()
		balance=html.find("balanceid")
		balanceline=html[balance:]
		euros=balanceline.split('&nbsp;')
		creditsleft=euros[1].split('</b>')
		final=creditsleft[0]
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
        elif account=="forthnet":#this means forthnet
		gethtml=foobar.response()
		html=gethtml.read()
                balance=html.find("<span id=\"SentItems1_lbPerDay\">")
                balanceline=html[balance:]
                temp1=balanceline.split("<span id=\"SentItems1_lbPerDay\">")
                temp2=temp1[1].split("</span>")
                temp3=temp2[0].split("/");
                final=str(5-int(temp3[0]))
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
	elif account!="otenet":
		foobar.select_form(nr=0)
	if account !="forthnet":
		foobar["username"] = username
        	foobar["password"] = password
	else:
		foobar["Username"] = username
		foobar["Password"] = password
	foobar.submit()
	if verbose:
		print "Verifying data.."
	pass #create a small delay
	ok=0
	testfoo=foobar
	try:
		leftcred=creditsleft(account,testfoo)
	except:
		sys.exit("Cannot login to "+account)
	if verbose:
		print "Logged in to "+account
		if account=="otenet" or account =="forthnet":
			print "SMS left: "+str(leftcred)
		elif account!="otenet" and account!="forthnet":
			print "Credits left: "+str(leftcred)
	if account=="otenet" or account=="forthnet":
		if leftcred=="0":
			sys.exit("You cant send more messages today")
	elif account!="otenet" and account!="forthnet":
		if leftcred<="0.03":
			sys.exit("You cant send more messages today")
	return leftcred


def sendsmscmd(account,username,password,number,message,verbose,leftcred):
	acc_page = acc_opensms[str(account)]#find page
	foobar.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]
	testfoo=foobar
	foobar.open(acc_page)
	if account=="otenet":
		try:
			foobar.select_form(name="sendform")

     		except:
        		sys.exit("Error contacting site... Please try again later\n")
	elif account!="otenet" and account!="forthnet":
		#do nothing
		pass
	elif account=="forthnet":
		try:
			foobar.select_form(nr=0)
		except:
			sys.exit("Error contacting site... Please try again later\n")
	if verbose:
		print "Creating message..."
	if account=="otenet":
		foobar["phone"] = number
       		foobar["message"] = message
	elif account=="forthnet":
		foobar["txtTo"] = number
		foobar["txtMessage"] = message
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
	if account=="otenet" or account=="forthnet":
		if verbose:
			print "Sending..."
		foobar.submit()
		if account=="otenet":
			leftcred2=creditsleft(account,testfoo,verbose)
		elif account=="forthnet":
			gethtml=foobar.response()
			html=gethtml.read()
			balance=html.find("<span id=\"lbPerDay\">")
			balanceline=html[balance:]
			temp1=balanceline.split("<span id=\"lbPerDay\">")
			temp2=temp1[1].split("</span>")
			temp3=temp2[0].split("/");
			leftcred2=5-int(temp3[0])
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
	#finish the job
	#if verbose show the report and exit with error code if the report is failure
	if final_report=="failure":
		if verbose:
			print "Report: "+final_report
		sys.exit("Failed to send message")
	else:
		if verbose:
			print "Report: "+final_report
		sys.exit(0)
