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
def myinsertaccount(f):
	f.ui.lineEdit.clear()
	f.ui.lineEdit2.clear()
	#insert username
	row=f.ui.tableWidget_2.currentItem()
	temp=row.text()
	accfile=open(ACCOUNTS+temp,"r")#open account file
	data=accfile.read()
	temp1=data.split()
	index=temp1[0]
	username=temp1[1]
	password=temp1[2]
	f.ui.comboBox.setCurrentIndex(int(index))
	f.ui.lineEdit.insert(username)
	f.ui.lineEdit2.insert(password)
		
