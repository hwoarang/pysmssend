from mydeletefile import *
from accountmanager import *
def mydeleteaccount(f):
	row=f.ui.tableWidget_2.currentItem()
	num=f.ui.tableWidget_2.currentRow()
	name=row.text()
	mydeletefile(f,name,num)
	createcombo(f.ui,0)
