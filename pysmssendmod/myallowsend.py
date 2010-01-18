def myallowsend(f,leftcred,account):
		# print leftcred
		if account != "otenet" and account != "forthnet":
			#this is how it works
			#if you have 0.05 credits on your account, you cant send a message.Ok?
			 if leftcred<"0.03":
				 f.ui.lineEdit3.setReadOnly(True)
				 f.ui.textEdit.setReadOnly(True)
				 f.ui.lineEdit3.clear()
				 f.ui.lineEdit3.insert("No credits left...")
				 f.ui.Send.setEnabled(False)
			 else:
			 	#other wise i am unlocking the buttons and now you can write your text
				 f.ui.lineEdit3.setReadOnly(False)
				 f.ui.textEdit.setReadOnly(False)
				 f.ui.textEdit.clear()
				 f.ui.Send.setEnabled(True)
				 f.ui.lineEdit3.clear()
		elif account=="otenet" or account=="forthnet":
		 	#same here, you must have more the 0 message left on your account. Obviously :P
			if leftcred=="0":
				f.ui.lineEdit3.setReadOnly(True)
				f.ui.textEdit.setReadOnly(True)
	 			f.ui.lineEdit3.clear()
				f.ui.lineEdit3.insert("No SMS left to send...")
				f.ui.Send.setEnabled(False)
			else:
				f.ui.textEdit.setReadOnly(False)
				f.ui.lineEdit3.setReadOnly(False)
				f.ui.textEdit.clear()
				f.ui.Send.setEnabled(True)
				f.ui.lineEdit3.clear()
