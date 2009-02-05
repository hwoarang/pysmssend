import sys
from pysmssendmod.tray import *
from mechanize import Browser
from pysmssendmod.creditsleft import *

acc_opensms = {
	'otenet':'http://tools.otenet.gr/tools/tiles/web2sms.do?showPage=smsSend&mnu=smenu23',
	'voipbuster':'https://myaccount.voipbuster.com/clx/index.php?part=menu&justloggedin=true',
	'voipdiscount':'https://myaccount.voipdiscount.com/clx/index.php?part=menu&justloggedin=true',
	'lowratevoip':'https://myaccount.lowratevoip.com/clx/index.php?part=menu&justloggedin=true',
	'voipbusterpro':'https://myaccount.voipbusterpro.com/clx/index.php?part=menu&justloggedin=true',
	'freevoip':'https://myaccount.freevoip.com/clx/index.php?part=menu&justloggedin=true',
	'12voip':'https://myaccount.12voip.com/clx/index.php?part=menu&justloggedin=true',
	'yahoo':'http://everywhere.yahoo.com/sms/sendsms',
	'webcalldirect':'https://myaccount.webcalldirect.com/clx/index.php?part=menu&justloggedin=true',
	'voipcheap':'https://myaccount.voipcheap.com/clx/index.php?part=menu&justloggedin=true',
	'nonoh':'https://myaccount.nonoh.net/clx/index.php?part=menu&justloggedin=true',
	'justvoip':'https://myaccount.justvoip.com/clx/index.php?part=menu&justloggedin=true'
	}
def mysmssend(foobar,f,tray,account,verbose,leftcred):
	acc_page = acc_opensms[str(account)]#find page
	foobar.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]
	testfoo=foobar
	foobar.open(acc_page)
	if verbose:
		print "Im opening -> "+acc_page+" \n"
	#if we have an otenet account 
	pass
	pass
	if verbose:
		print "I opened -> "+foobar.geturl()+" \n"
	if account == "otenet":
		try:
			foobar.select_form(name="sendform")
			
     		except:
        		sys.exit("Error contacting site... Please try again later\n")
	elif account != "otenet" and account != "yahoo":
		try:
			foobar.follow_link(text="Send a Text message (SMS)")
		except:
			try:
				foobar.follow_link(text="Send a Text Message (SMS)")
			except:
				sys.exit("Cannot open sms page. Please fill a bug ")
		foobar.select_form(nr=0)  
	else:#if yahoo
		try:
			foobar.select_form(nr=0)  
		except:
			sys.exit("Error contacting site... Please try again later\n")
	#get the number and the message	
	number=f.ui.lineEdit3.text()
        message2=f.ui.textEdit.toPlainText()  
	#convert Qstring to utf8
	message=message2.toUtf8()
	#fill the forms	
	if account=="otenet":
		foobar["phone"] = number
       		foobar["message"] = message
	elif account != "otenet" and account != "yahoo":
		foobar['bnrphonenumber'] =number
        	foobar['message'] = message
	elif account == "yahoo" :#this means yahoo
		foobar["ymsgSmsNumber"] = number
		foobar["ymsgSmsMessage"] = message
	#we need to convert qstring to plain text
	message=f.ui.textEdit.toPlainText()  
	#and then get the size of it
        size=message.length()
	try:
		#sumbit the stuff
         	foobar.submit()
		if verbose:
			print "Sending message ... \n"
		sent=1
	except:
        	f.ui.lineEdit_2.setText("Unknown error occured \n")
		sent=0
        if sent==1:
		#re-open the sms page and find credits left
		foobar.open(acc_page)#re open the sms page
		cred=creditsleft(f,account,foobar,verbose)
		if cred<leftcred:
			tray.showsentreport("Message was sent successfully :) ",1)
		else: #means something happend
			tray.showsentreport("Couldnt send message :(",0)
