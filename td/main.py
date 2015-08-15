# -*- coding: utf-8 -*-

import sys
import time
import quickfix as fix
import fix_app
#import wx

#print wx.VERSION_STRING

file = "./quickfix_it.ini"

settings = fix.SessionSettings( file )
application = fix_app.Application()
factory = fix.FileStoreFactory( "store" )
log = fix.FileLogFactory("log")
initiator = fix.SocketInitiator( application,factory, settings ,log )


initiator.start()
time.sleep( 4 )

Msg=fix.Message()
Msg.setString("8=FIX.4.29=18235=D34=1549=FIXTest12952=20141110-00:53:51.63856=SERVER11=Mon Nov 10 2014 08:53:51 GMT+080021=138=10040=244=39.1254=155=60044660=20140616-07:35:03.69610=251",0)
	
sessionID = fix.SessionID( "FIX.4.2","FIXTest129" ,"SERVER")

#print(sessionID)

fix.Session.sendToTarget( Msg,sessionID)
#fix.Session.sendToTarget( Msg)

while 1:
	time.sleep( 1 )
initiator.stop()