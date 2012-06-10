import os,stat
homedir=os.environ["HOME"]
from accountmanager import *
TEMPDIR="/.pysmssend/"
ACCOUNTS=homedir+TEMPDIR+"accounts/"
def mystoreaccount(f):
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
	os.chmod(ACCOUNTS+name, stat.S_IRUSR|stat.S_IWUSR)
	#Reconstruct manager
	createmanager(f.ui,0)
	createcombo(f.ui,0)
