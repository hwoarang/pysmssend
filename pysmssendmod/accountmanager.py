#!/usr/bin/env python
# -*- coding: utf-8 -*-
#***************************************************************************
#*    Pysmssend ( Source Code ) Account Manager functions
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
from PyQt4 import QtCore, QtGui
import os,sys,codecs,re
SHAREDIR="/usr/share/pysmssend/"
homedir=os.environ["HOME"]
TEMPDIR="/.pysmssend/"
ACCOUNTS=homedir+TEMPDIR+"accounts/"
debug=False

def filesindir(path):
	files=[]
	number=0
	for file in os.listdir(path):
		dirfile=os.path.join(path,file)
		if os.path.isfile(dirfile):
			files.append(dirfile)
			number=number+1
	return number,files

def createmanager(self,Form,want_gpg):
	num,x=filesindir(ACCOUNTS)
	#set number of lines
	self.tableWidget_2.setRowCount(num)
	#Clear the table
	self.tableWidget_2.clear()
	#Set title on the table
	headerItem2 = QtGui.QTableWidgetItem()
        headerItem2.setText(QtGui.QApplication.translate("Sent", "Account", None, QtGui.QApplication.UnicodeUTF8))
	for i in range(0,num):
		headerItem2 = QtGui.QTableWidgetItem()
		headerItem2.setText(QtGui.QApplication.translate("self",str(i+1), None, QtGui.QApplication.UnicodeUTF8))
		self.tableWidget_2.setVerticalHeaderItem(i,headerItem2)
		name1=x[i]
		name2=name1.split(ACCOUNTS)[1]

		item2 = QtGui.QTableWidgetItem()
		item2.setText(QtGui.QApplication.translate("self",
					str(name2).rstrip(".enc"),
					None,
					QtGui.QApplication.UnicodeUTF8))
		self.tableWidget_2.setItem(i,0,item2)
		
def createcombo(self,Form):
	num,x=filesindir(ACCOUNTS)
	self.comboBox_2.clear()
	self.comboBox_2.addItem(QtGui.QApplication.translate("Sent", "None", None, QtGui.QApplication.UnicodeUTF8))
	#Create combo box for accounts
	for i in range(0,num):
		name1=x[i]
		name2=name1.split(ACCOUNTS)[1]
		self.comboBox_2.addItem(QtGui.QApplication.translate("Sent", str(name2), None, QtGui.QApplication.UnicodeUTF8))
	

		
