#!/usr/bin/env python
# -*- coding: utf-8 -*-
#***************************************************************************
#*    Pysmssend  ( Source Code ) Gui
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

from designer.pysmssendgui import Ui_pysmssend_form
from designer.about import Ui_About
from designer.updates import Ui_Updates

class Sent(QtGui.QTabWidget, Ui_pysmssend_form):
	def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
		QtGui.QTabWidget.__init__(self)
		self.ui = Ui_pysmssend_form()
		self.ui.setupUi(self)
	def setup_version(self, version):
		self.setWindowTitle("pysmssend v"+version)

class About(QtGui.QTabWidget):
	def __init__(self):
		QtGui.QTabWidget.__init__(self)
		self.ui=Ui_About()
		self.ui.setupUi(self)
	def setup_version(self, version):
		tomatch = QtCore.QRegExp("pysmssend v[0-9]\\.[0-9][0-9]")
		tomatch.setMinimal(True)
		current_text = self.ui.AboutText.toHtml()
		current_text.replace(tomatch, 'pysmssend v'+version)
		self.ui.AboutText.setHtml(current_text)
		current_text = self.ui.AuthorsText.toHtml()
		current_text.replace(tomatch, 'pysmssend v'+version)
		self.ui.AuthorsText.setHtml(current_text)
		current_text = self.ui.ThanksText.toHtml()
		current_text.replace(tomatch, 'pysmssend v'+version)
		self.ui.ThanksText.setHtml(current_text)
		current_text = self.ui.AgreementText.toHtml()
		current_text.replace(tomatch, 'pysmssend v'+version)
		self.ui.AgreementText.setHtml(current_text)

class Updates(QtGui.QFrame, Ui_Updates):
	def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
		QtGui.QFrame.__init__(self)
		self.ui = Ui_Updates()
		self.ui.setupUi(self)
	def setText(self, text):
		self.ui.UpdatesText.setPlainText(text)
