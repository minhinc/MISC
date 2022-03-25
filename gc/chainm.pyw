import os,sys;sys.path.append(os.path.expanduser('~')+r'/tmp/')
import widgetm
import MISC.utillib.databasem as databasem
import getcontactm
import sendmailm
import dbpushpullm
widgeti=widgetm.scrolledtextc(None)
dbi=databasem.databasec(False)
getcontactm.getcontactc(dbpushpullm.dbpushpullc(sendmailm.sendmailc(None,widgeti,dbi),widgeti,dbi),widgeti,dbi).handle()
if __name__=='__main__': widgeti.mainloop()
dbi.close()
