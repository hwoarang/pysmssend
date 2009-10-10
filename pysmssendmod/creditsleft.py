#!/usr/bin/env python
# -*- coding: utf-8 -*-
#***************************************************************************
#*    Pysmssend  ( Source Code ) credits left
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

#really really cool function :P
#shows us how much money left on our account ( or messages for otenet
def creditsleft(f,account,foobar,verbose):
	if account != "otenet" and account != "forthnet":
		if verbose:
			print account+": Trying to find how much money left ...\n"
		gethtml=foobar.response()#get the html and parse it. Im not going to tell the details. tt us pure python
		html=gethtml.read()
		balance=html.find("balanceid")
		balanceline=html[balance:]
		euros=balanceline.split('&nbsp;')
		creditsleft=euros[1].split('</b>')
		final=creditsleft[0]
		f.ui.credits.setText("Credits Left : "+str(final))
		if verbose:
			print "you have "+final+" left...\n"
	elif account=="otenet":
		if verbose:
			print "Otenet: Trying to find how many messages you can send..\n"
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
		f.ui.credits.setText(str(final)+" sms left for today :-)")
		if verbose:
			print "you can send "+final+" messages ..\n"
	elif account=="forthnet":#this means forthnet
		if verbose:
			print "Forthnet: Retrieving credits...\n"
			gethtml=foobar.response()
			html=gethtml.read()
			balance=html.find("<span id=\"SentItems2Phase1_lbPerDay\">")
			balanceline=html[balance:]
			temp1=balanceline.split("<span id=\"SentItems2Phase1_lbPerDay\">")
			temp2=temp1[1].split("</span>")
			temp3=temp2[0].split("/");
			final=str(5-int(temp3[0]))
			f.ui.credits.setText(str(final)+" sms left for today :-)")
	#final is the amount of money we have :)		
	return final
