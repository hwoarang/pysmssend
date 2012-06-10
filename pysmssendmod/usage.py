#!/usr/bin/env python
# -*- coding: utf-8 -*-
#***************************************************************************
#*    Pysmssend ( Source Code ) Help message for command line utility
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

def usage():                                            
	print """
		pysmssend         Send SMS over the Internet
        
		type 'pysmssend' for Gui interface
		
		if you want command line options use pysmssendcmd or pysmssend
		pysmssendcmd [-h] -a <account> -u <username> -p <password> -n <number> <"text to send">
		example: pysmssend -a otenet -u foo -p bar -n 123456 "Hello World!"

  		-h                  print this message
  		-a <account>        Account name: <otenet|voipbuster|voipdiscount|voipbusterpro|lowratevoip|
				    12voip|freevoip|forthnet|webcalldirect|pennytel>
  		-u <username>       username
  		-p <password>       password
  		-n <number>         Telephone Number
  		-v                  Verbose mode (useful for debugging)


				Homepage: http://pysmssend.silverarrow.org
		"""
