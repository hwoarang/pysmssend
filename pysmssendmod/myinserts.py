import os
homedir=os.environ["HOME"]
TEMPDIR="/.pysmssend/"
ACCOUNTS=homedir+TEMPDIR+"accounts/"
##Insert Number
def myinsert(f):
	f.ui.lineEdit3.clear()
	row=f.ui.tableWidget.currentItem()
	number=row.text()
	f.ui.lineEdit3.insert(number)
	


	#insert Account
def myinsertaccount(f,want_gpg):
	f.ui.lineEdit.clear()
	f.ui.lineEdit2.clear()
	#insert username
	row=f.ui.tableWidget_2.currentItem()
	temp=row.text()
	if want_gpg:
		temp = temp + ".enc"
	full_name =  ACCOUNTS+temp
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
			with open(full_name) as afile:
				afile = afile.read()
				data = gpg.decrypt(afile)
				data = data.data				
		except IOError as e:
			print e.strerror
	else:
		accfile=open(data, "r")#open account file
		data=accfile.read()
	temp1=data.split()
	index=temp1[0]
	username=temp1[1]
	password=temp1[2]
	f.ui.comboBox.setCurrentIndex(int(index))
	f.ui.lineEdit.insert(username)
	f.ui.lineEdit2.insert(password)
		
