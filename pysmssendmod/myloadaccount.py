#!/usr/bin/env python
# -*- coding: utf-8 -*-
#***************************************************************************
#*    Pysmssend ( Source Code ) Load account
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
import os
from PyQt4 import QtCore, QtGui
#seting variables
homedir=os.environ["HOME"]
TEMPDIR="/.pysmssend/"
ACCOUNTS=homedir+TEMPDIR+"accounts/"

def myloadaccount(f,verbose):
	homedir=os.environ["HOME"]#read home directory
	f.ui.credits.clear() #clear Credits
	f.ui.lineEdit.clear()#clear username field
	f.ui.lineEdit2.clear()#clear password field
	f.ui.Result1.clear()#clear result field
	try:
		choice=f.ui.comboBox.currentText()#read account
		choice=str.lower(str(choice))
		if verbose:
			print("searching for "+choice+" stored account...\n")
		data=open(homedir+TEMPDIR+choice,"r")#open account file
		if verbose:
			print("I found stored account...\n")
		account=data.read()#read it
		infos=account.split()
		if verbose:
			print("inserting data to the fields...\n")
		f.ui.lineEdit.insert(infos[0])#parse the infos on the fields
		f.ui.lineEdit2.insert(infos[1])
	except:
		pass
	
#this function is used due to account manager
def myloadstoredaccount(f,verbose):
	homedir=os.environ["HOME"]#read home directory
	f.ui.lineEdit.clear()#clear username field
	f.ui.lineEdit2.clear()#clear password field
	try:
		choice=f.ui.comboBox_2.currentText()#read account
		if choice!="None":
			if verbose:
				print("importing "+choice+" account...\n")
			#read index of account
			index=f.ui.comboBox_2.currentIndex()			#insert username
			row=f.ui.tableWidget_2.item(index-1,0)
			temp=row.text()
			accfile=open(ACCOUNTS+temp,"r")#open account file
			data=accfile.read()
			temp1=data.split()
			index=temp1[0]
			username=temp1[1]
			passwd=temp1[2]
			f.ui.comboBox.setCurrentIndex(int(index))
			f.ui.lineEdit.insert(username)
			f.ui.lineEdit2.insert(passwd)
			if verbose:
				print("successfully imported "+choice+"...\n")
		else:
			f.ui.lineEdit.clear()#clear username field
			f.ui.lineEdit2.clear()#clear password field
	except:
		pass
	
