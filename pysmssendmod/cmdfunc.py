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
import sys,time
import urllib2,urllib
foobar = Browser()
foobar.set_handle_robots(False)


##################### CREDITS LEFT ###############################
def creditsleft(account,foobar,verbose):
	if verbose:
		print "Retrieving remaining credits..."
	if account != "otenet" and account != "forthnet" and account != "voipbuster" and account != "lowratevoip":
		gethtml=foobar.response()#get the html and parse it. Im not going to tell the details.
		html=gethtml.read()
		balance=html.find("balanceid")
		balanceline=html[balance:]
		euros=balanceline.split('&nbsp;')
		creditsleft=euros[1].split('</b>')
		final=str(creditsleft[0])
	elif account == "voipbuster" or account == "lowratevoip":
		gethtml=foobar.response()
		html=gethtml.read()
		balance=html.find("balance-section")
		balanceline=html[balance:]
		euros=balanceline.split('balance')
		euros=euros[3].split(' ')
		euros=euros[1].split("</span>")
		final=str(euros[0])
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
		final=str(int(left[0]))
        elif account=="forthnet":
		gethtml=foobar.response()
		html=gethtml.read()
                balance=html.find("<span id=\"SentItems2Phase1_lbPerMonth\">")
       	        balanceline=html[balance:]
               	temp1=balanceline.split("<span id=\"SentItems2Phase1_lbPerMonth\">")
       	        temp2=temp1[1].split("</span>")
                temp3=temp2[0].split("/");
		print temp3
               	final=str(int(temp3[0]))
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
	try:
		if verbose:
			print "Opening url --> "+login_page
		foobar.open(login_page)#open url
	except:
		sys.exit("ERROR: Check your internet connection and try again...")
	if verbose:
		print "Connection established"
	if account=="otenet":
		foobar.select_form(name="loginform")
	elif account!="otenet":
		foobar.select_form(nr=0)
	if account == "voipbuster" or account == "lowratevoip":
		foobar["login[username]"] = username
		foobar["login[password]"] = password
	elif account != "forthnet":
		foobar["username"] = username
		foobar["password"] = password
	else:
		foobar["Username"] = username
		foobar["Password"] = password
	try:
		if verbose:
			print "Verifying data..."
		foobar.submit()
	except:
		sys.exit("ERROR: Check your internet connection and try again...")
	time.sleep(2) #create a small delay
	ok=0
	testfoo=foobar
	repeat=0
	while repeat<=2:# Do 3 login attemps just in case there is a network error or smth
		try:
			time.sleep(1)
			leftcred=creditsleft(account,testfoo,verbose)
			break
		except:
			repeat=repeat+1# increase login attemps
			if repeat <= 3:
				if verbose:
					print "Retrying to login...("+str(repeat)+"/3)"
			else:# in case all of them failed
				sys.exit("Cannot login to "+account+". Invalid credentials or network error. Please try again :-)")
	if verbose:
		print "Logged in to "+account
		if account=="otenet" or account =="forthnet":
			print "SMS left: "+str(leftcred)
		elif account!="otenet" and account!="forthnet":
			print "Credits left: "+str(leftcred)
	if leftcred<="0.03":
		sys.exit("You cant send more messages today :-(")
	return leftcred


def sendsmscmd(account,username,password,number,message,verbose,leftcred):
	if account == "otenet" or account == "forthnet":
		acc_page = acc_opensms[str(account)]#find page
		foobar.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]
		testfoo=foobar
		foobar.open(acc_page)
	if verbose:
		print "Creating message..."
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
	if account=="otenet":
		foobar["phone"] = number
       		foobar["message"] = message
	elif account=="forthnet":
		foobar["txtTo"] = number
		foobar["txtMessage"] = message
	else:
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
			leftcred2=str(5-int(temp3[0]))
		if leftcred==leftcred2:#if we have the same messages after the submit
			#it means that we didnt send the message
			#set final_report
			final_report=="failure"
		else:
			final_report=="success"
        else:
		if verbose:
			print "Sending..."
		req = urllib2.Request(acc_opensms2[str(account)]+data, headers=headers)
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
