
import sys,signal 
import os
import getopt
from mechanize import Browser 

SHAREDIR="/usr/share/pysmssend/"
TEMPDIR="/.pysmssend/"
verbose = False
foobar = Browser()
foobar.set_handle_robots(False)

acc_openlogin = {
	'otenet':'http://tools.otenet.gr/tools/index.do',
	'voipbuster':'https://myaccount.voipbuster.com/clx/index.php?part=plogin&username=Znexbf6430&password=',
	'voipdiscount':'https://myaccount.voipdiscount.com/clx/index.php?part=plogin&username=Znexbf6430&password=',
	'lowratevoip':'https://myaccount.lowratevoip.com/clx/index.php?part=plogin&username=Znexbf6430&password=',	
	'voipbusterpro':'https://myaccount.voipbusterpro.com/clx/index.php?part=plogin&username=Znexbf6430&password=',
	'voipcheap':'https://myaccount.voipcheap.com/clx/index.php?part=plogin&username=Znexbf6430&password=',
	'freevoip':'https://myaccount.freevoip.com/clx/index.php?part=plogin&username=Znexbf6430&password=',
	'nonoh':'https://myaccount.nonoh.com/clx/index.php?part=plogin&username=Znexbf6430&password=',	
	'justvoip':'https://myaccount.justvoip.com/clx/index.php?part=plogin&username=Znexbf6430&password=',
	'12voip':'https://myaccount.12voip.com/clx/index.php?part=plogin&username=Znexbf6430&password=',	
	'webcalldirect':'https://myaccount.webcalldirect.com/clx/index.php?part=plogin&username=Znexbf6430&password='
		}	
acc_opensms = {
	'otenet':'http://tools.otenet.gr/tools/tiles/web2sms.do?showPage=smsSend&mnu=smenu23',
	'voipbuster':'https://myaccount.voipbuster.com/clx/index.php?part=menu&justloggedin=true',
	'voipdiscount':'https://myaccount.voipdiscount.com/clx/index.php?part=menu&justloggedin=true',
	'lowratevoip':'https://myaccount.lowratevoip.com/clx/index.php?part=menu&justloggedin=true',
	'voipbusterpro':'https://myaccount.voipbusterpro.com/clx/index.php?part=menu&justloggedin=true',
	'voipcheap':'https://myaccount.voipcheap.com/clx/index.php?part=menu&justloggedin=true',
	'nonoh':'https://myaccount.nonoh.com/clx/index.php?part=menu&justloggedin=true',
	'justvoip':'https://myaccount.justvoip.com/clx/index.php?part=menu&justloggedin=true',
	'12voip':'https://myaccount.12voip.com/clx/index.php?part=menu&justloggedin=true',
	'yahoo':'http://everywhere.yahoo.com/sms/sendsms',
	'webcalldirect':'https://myaccount.webcalldirect.com/clx/index.php?part=menu&justloggedin=true'
	      }

	
	
def usage():                                            
		print """
	pysmssend         Send SMS over the Internet

	pysmssend [-h] -a <account> -u <username> -p <password> -n <number> <"text to send">
	example: pysmssend -a otenet -u foo -p bar -n 123456 "Hello World!"
	
  	-h                  print this message

  	-a <account>        Account name: <otenet|voipbuster|voipdiscount|voipbusterpro|lowratevoip|12voip|freevoip|yahoo|webcalldirect>
  	-u <username>       Username
  	-p <password>       Password
  	-n <number>         Telephone Number
	-v 		    Verbose
	
	 Homepage: http://pysmssend.sourceforge.net

		"""

def cmdlogin(account,username,password,verbose):
	testfoo = Browser()
	testfoo.set_handle_robots(False)
	if account!="yahoo":
		login_page=acc_openlogin.get(account)
		foobar.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]
		testfoo.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]
        	foobar.open(login_page)
		if account == "otenet":
			foobar.select_form(name="loginform")
		if account != "otenet" and account != "yahoo":
			foobar.select_form(nr=0)
        	foobar["username"] = username
               	foobar["password"] = password
		if verbose:
	       		print "Verifying Data..."
		foobar.submit()
		try:
			#Try to open sms page (this helps on deciding if login was correct )
			if account=="otenet":
				acc_page="http://tools.otenet.gr/tools/tiles/Intro/generalIntro.do"
			else:
				acc_page = acc_opensms[str(account)]#find sms page
			testfoo=foobar
			foobar.open(acc_page)#open sms page
			leftcred=cmdcreditsleft(account,testfoo)
			test=foobar.geturl()
			if test==acc_page:
				ok=1
			else:pass
		except:
			sys.exit("Login Failed.")
		if ok==1:
			ok=0
			if verbose:
	      			print "Login Successfully"
			leftcred=cmdcreditsleft(account,foobar)
			if account=="otenet":
				if verbose: print "Messages left: "+leftcred 
				if leftcred=="0":
					sys.exit("Sorry, no sms left to send")
			if account != "otenet" and account != "yahoo":
				if verbose: print "Credits :"+leftcred
				if leftcred<"0.05":
					sys.exit("Sorry, no credits left on your account")
	return leftcred			

def sendsmscmd(account,username,password,phone,text,verbose):
	acc_page = acc_opensms.get(account)
	if not acc_page:
		usage()
		sys.exit("No valid account specified")
	leftcred=cmdlogin(account,username,password,verbose)
	foobar.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]
	foobar.open(acc_page)
	if account == "otenet":
		try:
			foobar.select_form(name="sendform")
       		except:
           		sys.exit("Problem filling otenet sms form. Exiting.")
		foobar["phone"] = phone
	       	foobar["message"] = text
	elif account != "otenet"  and account != "yahoo":
		try:
		      	foobar.follow_link(text="Send a Text message (SMS)")
		except:
			try:
				foobar.follow_link(text="Send a Text Message (SMS)")
			except:
				sys.exit("Problem filling sms form. Exiting.")
		foobar.select_form(nr=0)  
		foobar['bnrphonenumber'] = phone
       		foobar['message'] = text
	else:#if yahoo
		foobar["ymsgSmsNumber"] = number
		foobar["ymsgSmsMessage"] = message
	if verbose:
        	print "Sending SMS..."
       	try:
        	foobar.submit()
		#find leftmessages
		foobar.open(acc_page)
		cred=cmdcreditsleft(account,foobar)
		if cred<leftcred:
			if verbose:
           			print "Message Sent."
		else:
			sys.exit("Failure... Couldnt send message")
       	except:
        	sys.exit("Failure...Text message too long?")
	
		##Credits left
def cmdcreditsleft(account,foobar):
	if account != "otenet" and account != "yahoo":
		gethtml=foobar.response()
		html=gethtml.read()
		balance=html.find("balanceid")
		balanceline=html[balance:]
		euros=balanceline.split('&nbsp;')
		creditsleft=euros[1].split('</b>')
		left=creditsleft[0]
	elif account=="otenet":
		foobar.open("http://tools.otenet.gr/tools/tiles/Intro/generalIntro.do")
		gethtml=foobar.response()
		html=gethtml.read()
		balance=html.find("""  <a href="/tools/tiles/web2sms.do?showPage=smsSend&amp;mnu=smenu23"> <span class="txtmov10b_yellow">""")
		#print balance
		balanceline=html[balance:]
		data=balanceline.split()
		dataline=data[3]
		temp1=dataline.split("""class="txtmov10b_yellow">""")
		temp2=temp1[1]
		left2=temp2.split("</span>")
		left=left2[0]
	final=left
	return final
