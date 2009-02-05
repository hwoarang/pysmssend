import os
homedir=os.environ["HOME"]
TEMPDIR="/.pysmssend/"
ACCOUNTS=homedir+TEMPDIR+"accounts/"
def mydeletefile(f,name,num):
	for file in os.listdir(ACCOUNTS):
		dirfile=os.path.join(ACCOUNTS,file)
		if dirfile==ACCOUNTS+name:
			os.remove(ACCOUNTS+name)
			f.ui.tableWidget_2.removeRow(num)