#!/usr/bin/env python
# -*- coding: utf-8 -*-
#***************************************************************************
#*    Pysmssend  ( Source Code ) Addressbook functions
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
from subprocess import  Popen,PIPE
SHAREDIR="/usr/share/pysmssend/"
TEMPDIR="/.pysmssend/"
def getdata(self,Form,verbose):
	debug=verbose
	found=0
	return_code=254
	global tilfwno3,num_lines,homedir   
	if debug:
		print("\nBuilding Addressbook ... \n")
		print("Creating Temp Files ...\n\n Wait...\n")
	homedir=os.environ["HOME"]
	#this may vary according to KDE version. We need to specify which kde is running
	if debug:
		print("Trying to find the kaddressbook contacts' path...\n")
	if os.path.exists(homedir+"/.kde4/share/apps/kabc/std.vcf"):
		if debug:
			print("Found contacts under .kde4/share/apps/kabc/ folder\n")
		addresspath=".kde4"
		found=1
	elif os.path.exists(homedir+"/.kde/share/apps/kabc/std.vcf"):
		if debug:
			print("Found contacts under .kde/share/apps/kabc/ folder\n")
		addresspath=".kde"
		found=1
	else:
		if debug:     print("Kaddressbook contacts not found... \n\n")
		num_lines=0
		self.retranslateUi(Form,num_lines)

	if found:     
		if debug:
			print("Found Kaddressbook contacts ...\n\n")
			print("opening "+homedir+"/"+addresspath+"/share/apps/kabc/std.vcf")	
		try:  filestd = open(homedir+"/"+addresspath+"/share/apps/kabc/std.vcf","r")
		except IOError: sys.exit("Can't open file std.vcf")
		text = filestd.readlines()
		filestd.close()
		keyword = re.compile(r"N:")
		keyword2 = re.compile(r"TYPE=CELL:")
		nameslist=[]
		numlist=[]
		for line in text:
			if keyword.search (line):
				nameline=line
				if debug: print(line)
			if keyword2.search (line):
				nameslist.append(nameline)
				numlist.append(line)
				if debug: print(line)
		    	    
		lena = len(nameslist)
		lenb = len(numlist)
		num_lines=lenb
		self.retranslateUi(Form,num_lines)

		mycounter=0
		while mycounter < lenb:
			headerItem = QtGui.QTableWidgetItem()
			headerItem.setText(QtGui.QApplication.translate("self",str(mycounter+1), None, QtGui.QApplication.UnicodeUTF8))
			self.tableWidget.setVerticalHeaderItem(mycounter,headerItem)
			
			name=nameslist[mycounter]
			
			name=name.replace('N:','')
			name=name.replace(';;;','')
			name=name.replace(';',' ')
			name=name[:-2]
			item = QtGui.QTableWidgetItem()
			item.setText(QtGui.QApplication.translate("self", str(name), None, QtGui.QApplication.UnicodeUTF8))
			self.tableWidget.setItem(mycounter,0,item)
			tel=numlist[mycounter]
			tel=tel.replace('TEL;TYPE=CELL:','')
			tel=tel.encode('iso-8859-7')
			tel=tel[:-2]
			i=0
			flag=0
			item = QtGui.QTableWidgetItem()
			item.setText(QtGui.QApplication.translate("self", str(tel), None, QtGui.QApplication.UnicodeUTF8))
			self.tableWidget.setItem(mycounter,1,item)
			mycounter=mycounter+1
		if debug:     print("Finished\n\n")
