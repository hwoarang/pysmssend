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
import os, stat
from PyQt4 import QtCore, QtGui
from accountmanager import *

#Variables
homedir=os.environ["HOME"]
TEMPDIR="/.pysmssend/"
ACCOUNTS=homedir+TEMPDIR+"accounts/"

def myloadaccount(f,verbose,want_gpg,gpg_key):
	"""
	Called everytime the user selects a different provider from the
	drop-down menu
	"""
	homedir = os.environ["HOME"]#read home directory
	f.ui.credits.clear() #clear Credits
	f.ui.lineEdit.clear()#clear username field
	f.ui.lineEdit2.clear()#clear password field
	f.ui.Result1.clear()#clear result field
	choice = f.ui.comboBox.currentText()#read account
	choice = str.lower(str(choice))
	if want_gpg:
		choice = choice+".enc"
	if verbose:
		print "Searching for existing "+choice+" account...\n"
	full_choice = homedir+TEMPDIR+choice
	if os.path.isfile(full_choice):
		if verbose:
			print "Found it!\n"
		if want_gpg:
			try:
				import gnupg
			except ImportError:
				print "I can't import the gnupg module"
				print "Make sure it's installed"
				sys.exit(1)
			gpg = gnupg.GPG()
			gpg.encoding = 'utf-8'
			try:
				with open(full_choice) as afile:
					afile = afile.read()
					data = gpg.decrypt(afile)
					account = data.data				
			except IOError as e:
				print e.strerror
		else:
			data = open(full_choice,"r")#open account file
			account = data.read()#read it
		infos = account.split()
		if verbose:
			print "Loading account information...\n"
		f.ui.lineEdit.insert(infos[0])#parse the infos on the fields
		f.ui.lineEdit2.insert(infos[1])
	
def myloadstoredaccount(f,verbose):
	homedir=os.environ["HOME"]#read home directory
	f.ui.lineEdit.clear()#clear username field
	f.ui.lineEdit2.clear()#clear password field
	try:
		choice=f.ui.comboBox_2.currentText()#read account
		if choice!="None":
			if verbose:
				print "importing "+choice+" account...\n"
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
				print "successfully imported "+choice+"...\n"
		else:
			f.ui.lineEdit.clear()#clear username field
			f.ui.lineEdit2.clear()#clear password field
	except:
		pass

def mystoreaccount(f,want_gpg,gpg_key):
	#read account
	account=f.ui.comboBox_3.currentIndex()
	#read username
	username=f.ui.lineEdit_6.text()
	#read password
	password=f.ui.lineEdit_7.text()
	#read custom name
	name=f.ui.lineEdit_4.text()
	file=open(ACCOUNTS+name,"w")
	file.write(str(account)+"\n")
	file.write(str(username)+"\n")
	file.write(str(password)+"\n")
	file.close()
	if want_gpg:
		try:
			import gnupg
		except ImportError:
			print "I can't import the gnupg module"
			print "Make sure it's installed"
			sys.exit(1)
		gpg = gnupg.GPG()
		gpg.encoding = 'utf-8'
		try:
			with open(ACCOUNTS+name) as afile:
				gpg.encrypt_file(afile,
							recipients=gpg_key,
							output=ACCOUNTS+name+".enc")
				os.remove(ACCOUNTS+name)
				name = name + ".enc"
		except IOError as e:
			print e.strerror
	os.chmod(ACCOUNTS+name, stat.S_IRUSR|stat.S_IWUSR)
	#Reconstruct manager
	createmanager(f.ui,0,want_gpg)
	createcombo(f.ui,0)

def mydeleteaccount(f, verbose, want_gpg):
	row = f.ui.tableWidget_2.currentItem()
	num = f.ui.tableWidget_2.currentRow()
	name = row.text()
	if want_gpg:
		name = name + ".enc"
	for file in os.listdir(ACCOUNTS):
		dirfile=os.path.join(ACCOUNTS,file)
		if dirfile == ACCOUNTS+name:
			if verbose:
				print "Removing "+name
			os.remove(ACCOUNTS+name)
			if verbose:
				print "Done"
			f.ui.tableWidget_2.removeRow(num)
	createcombo(f.ui,0)
