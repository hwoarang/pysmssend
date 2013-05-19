#!/usr/bin/env python
# -*- coding: utf-8 -*-
#***************************************************************************
#*    Pysmssend  ( Source Code ) input_validation
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

def myallowsend(f,leftcred,account):
		# print leftcred
		if account != "otenet" and account != "forthnet":
			#this is how it works
			#if you have 0.05 credits on your account, you cant send a message.Ok?
			 if leftcred<"0.03":
				 f.ui.lineEdit3.setReadOnly(True)
				 f.ui.textEdit.setReadOnly(True)
				 f.ui.lineEdit3.clear()
				 f.ui.lineEdit3.insert("No credits left...")
				 f.ui.Send.setEnabled(False)
			 else:
			 	#other wise i am unlocking the buttons and now you can write your text
				 f.ui.lineEdit3.setReadOnly(False)
				 f.ui.textEdit.setReadOnly(False)
				 f.ui.textEdit.clear()
				 f.ui.Send.setEnabled(True)
				 f.ui.lineEdit3.clear()
		elif account=="otenet" or account=="forthnet":
		 	#same here, you must have more the 0 message left on your account. Obviously :P
			if leftcred=="0":
				f.ui.lineEdit3.setReadOnly(True)
				f.ui.textEdit.setReadOnly(True)
	 			f.ui.lineEdit3.clear()
				f.ui.lineEdit3.insert("No SMS left to send...")
				f.ui.Send.setEnabled(False)
			else:
				f.ui.textEdit.setReadOnly(False)
				f.ui.lineEdit3.setReadOnly(False)
				f.ui.textEdit.clear()
				f.ui.Send.setEnabled(True)
				f.ui.lineEdit3.clear()

def mychecklength(f):
	"""Real-time message length display"""
	choice=f.ui.comboBox.currentText()#read account
	choice=str.lower(str(choice))#lower the string
	message=f.ui.textEdit.toPlainText()  #get message text
	size=message.length()#read message length
	if choice != "otenet":
		left=160-size
		length2=str(left)
		if left >=0:
			f.ui.lineEdit_3.clear()#clear size area
			f.ui.lineEdit_3.setText(length2)#set the new size
			#enable send button
			f.ui.Send.setEnabled(True)
		elif left <0:
			f.ui.lineEdit_3.setText("Above Limit: "+length2)
			f.ui.Send.setEnabled(False)
	elif choice=="otenet":#for otenet characters must be less than 145-username
		username=f.ui.lineEdit.text()#read the user name
		left=145-len(username) -size
		length2=str(left)
		#left2=left-size
		if left >=0:
			f.ui.lineEdit_3.clear()
			f.ui.lineEdit_3.setText(length2)
			f.ui.Send.setEnabled(True)
		elif left <0:
			f.ui.lineEdit_3.setText("Above Limit: "+length2)
			f.ui.Send.setEnabled(False)
