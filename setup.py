#!/usr/bin/env python
# -*- coding: utf-8 -*-
#***************************************************************************
#*    Pysmssend ( Source Code ) setup.py
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

from distutils.core import setup
setup(name='pysmssend',
    version='1.48',
    description='Send SMS over the Internet',
    author='Markos Chandras',
    author_email='hwoarang@silverarrow.org',
    license='GPLv3',
    url='http://pysmssend.silverarrow.org',
    py_modules=['pysmssendmod/__init__',
'pysmssendmod/about',
'pysmssendmod/addressfunc',
'pysmssendmod/pysmssendgui',
'pysmssendmod/accountmanager',
'pysmssendmod/tray',
'pysmssendmod/updater',
'pysmssendmod/account_io',
'pysmssendmod/core_io',
'pysmssendmod/usage',
'pysmssendmod/sites',
'pysmssendmod/cmdfunc',
'pysmssendmod/input_validation'])
