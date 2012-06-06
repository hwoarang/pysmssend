#!/bin/bash
#***************************************************************************
#*    Pysmssend  ( Source Code ) Uninstall script
#***************************************************************************
echo -e "\n\nUnistalling Pysmssend from your system \n\n"
echo -e "Removing files...\n"
rm -rf /usr/share/pysmssend/
a=`python -V 2>&1`
b=`echo $a|cut -d '.' -f 2`
# is there a .pysmssend_install.txt file?
if [[ -e .pysmssend_install.txt ]]; then
	cat .pysmssend_install.txt | xargs rm -r
else
	# Try to guess
	if [[ -d /usr/lib/python2.$b/site-packages/pysmssendmod ]]; then
		rm -r /usr/lib/python2.$b/site-packages/pysmssendmod/
	elif [[ -d /usr/local/lib/python2.$b/site-packages/pysmssendmod ]]; then
		rm -r /usr/local/lib/python2.$b/site-pacakges/pysmssendmod/
	fi
	rm -r /usr/share/pysmssend
	rm /usr/share/pixmaps/pysmssend.png
	rm /usr/bin/pysmssend
	rm /usr/bin/pysmssendcmd
	rm /usr/share/applications/pysmssend.desktop
fi
echo -e "Please remember to remove .pysmssend folder from your home directory\n\n"
echo -e "Thank you for using the program \n\n"
