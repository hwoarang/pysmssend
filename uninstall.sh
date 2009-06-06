#!/bin/bash
#***************************************************************************
#*    Pysmssend  ( Source Code ) Uninstall script
#***************************************************************************
echo -e "\n\nUnistalling Pysmssend from your system \n\n"
echo -e "Removing files...\n"
rm -rf /usr/share/pysmssend/
a=`python -V 2>&1`
b=`echo $a|sed -e s/^.........//|sed -e s/..$//`
rm -rf /usr/lib/python2.$b/site-packages/pysmssendmod/
rm -rf /usr/local/lib/python2.$b/site-packages/pysmssendmod/
rm /usr/share/pixmaps/pysmssend.png
rm /usr/bin/pysmssend
rm /usr/bin/pysmssendcmd
rm /usr/share/applications/pysmssend.desktop
echo -e "Please remember to remove .pysmssend folder from your home directory\n\n"
echo -e "Thank you for using the program \n\n"
