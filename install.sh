#!/bin/bash
#***************************************************************************
#*    Pysmssend ( Source Code ) Install Script
#***************************************************************************
echo -e "\n\n\n***** Installing Pysmssend ******\n\n"
echo -e "Creating Directory...\n"
mkdir -p /usr/share/pysmssend/
echo -e "******    Done    ****** \n"
echo -e "Copying Files...\n"
cp -R Icons /usr/share/pysmssend/
cp /usr/share/pysmssend/Icons/pysmssend.png /usr/share/pixmaps/
echo -e "Building python modules...\n"
python setup.py build
echo -e "\n Done \n "
echo -e "installing python modules...\n"
python setup.py install
echo -e "\n ******    Done    ****** \n"
cp pysmssend /usr/bin/
cp pysmssendcmd /usr/bin/
cp pysmssend.desktop /usr/share/applications/
echo -e " *** Installation Completed Successfully *** \n\n\n\n"
echo -e " ************** IMPORTANT!!! *************** \n"
echo -e " Please make sure that you have PyQt4 (for gui support)"
echo -e " and python-mechanize installed\n"
echo -e "####################### INFO ###########################"
echo -e "#   Run the program using pysmssend command            #"
echo -e "#   Use -h parameter to see the help file              #"
echo -e "#   Please read the README file first for proper use   #"
echo -e "#   Homepage: http://pysmssend.silverarrow.org		#"
echo -e "#   Bug Reports :  hwoarang@silverarrow.org		#"
echo    "########################################################"
