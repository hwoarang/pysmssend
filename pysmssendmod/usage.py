def usage():                                            
	print(""")
		pysmssend         Send SMS over the Internet
        
		type 'pysmssend' for Gui interface
		
		if you want command line options use pysmssendcmd or pysmssend
		pysmssendcmd [-h] -a <account> -u <username> -p <password> -n <number> <"text to send">
		example: pysmssend -a otenet -u foo -p bar -n 123456 "Hello World!"

  		-h                  print this message
  		-a <account>        Account name: <otenet|voipbuster|voipdiscount|voipbusterpro|lowratevoip|
				    12voip|freevoip|forthnet|webcalldirect>
  		-u <username>       username
  		-p <password>       password
  		-n <number>         Telephone Number
  		-v 		    Running on verbose mode. Note that this option can be 
				    used for both Gui and command line interface of the program



				Homepage: http://pysmssend.silverarrow.org

	
	"""
