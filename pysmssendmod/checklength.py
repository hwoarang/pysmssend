#!/usr/bin/env python
# -*- coding: utf-8 -*-
#***************************************************************************
#*    Pysmssend  ( Source Code ) CheckLength
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
def mychecklength(f):#takes the gui as an argument
	choice=f.ui.comboBox.currentText()#read account
	choice=str.lower(str(choice))#lower the string
	message=f.ui.textEdit.toPlainText()  #get message text
	size=message.length()#read message length
	if choice != "otenet" and choice != "yahoo":
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
    
