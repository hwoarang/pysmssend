4 #!/usr/bin/env python
# -*- coding: utf-8 -*-
#***************************************************************************
#*    Pysmssend ( Source Code ) Addressbook functions
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
from pysmssendmod.pysmssendgui import Ui_Sent, Testmain
SHAREDIR="/usr/share/pysmssend/"

class trayicon:
	def start(self):
		#Create Icon
		icon=QtGui.QIcon(SHAREDIR+"Icons/pysmssend.png")
		exiticon=QtGui.QIcon(SHAREDIR+"Icons/exit.png")
		abouticon=QtGui.QIcon(SHAREDIR+"Icons/book.png")
		updateicon=QtGui.QIcon(SHAREDIR+"Icons/update.png")
		self.trayic=QtGui.QSystemTrayIcon(icon)	
		#Implement Actions
		global ActionsMenu
		ActionsMenu=QtGui.QMenu()
		self.trayic.Updater=ActionsMenu.addAction(updateicon,"Check for updates")
		self.trayic.About=ActionsMenu.addAction(abouticon,"About")
		ActionsMenu.addSeparator()
		self.trayic.Exit=ActionsMenu.addAction(exiticon,"Quit Pysmssend")
		self.trayic.setContextMenu(ActionsMenu)
		self.trayic.show()
		self.trayic.setToolTip("Pysmssend 1.41")

	def showsentreport(self,message,status):
		self.status=status
		if self.status==1:
			self.trayic.showMessage("Report",message,self.trayic.Information,6000)
		else:
			self.trayic.showMessage("Report",message,self.trayic.Warning,6000)

	def showlogin(self,account,status):	
		self.status=status
		if self.status==1:
			self.trayic.showMessage("","Logged in to "+account,self.trayic.Information,6000)
		else:
			self.trayic.showMessage("","Login to "+account+" failed",self.trayic.Warning,6000)
	def yahooinfo(trayic):
		trayic.showMessage("","Logged in to Yahoo. Please remember that Yahoo charges the recipient with standar rates . Please refer to http://everywhere.yahoo.com/sms/sendsms for more information",trayic.Information,15000)

	def hidemain(gui):
		gui.hide()

	def showmain(gui):
		gui.show()
