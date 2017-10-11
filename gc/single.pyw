import widgetm
import getcontactm
import sendmailm
widgeti=widgetm.scrolledtextc()
sendmailm.sendmailc(None,widgeti).handle()
if __name__=='__main__': widgeti.mainloop()
