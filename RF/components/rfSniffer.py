import drivers.rf
import app
from entities import *
import datetime

class rfSniffer(object):
    def __init__(self):
        drivers.rf.addCodeListener(self)
        self.__lastCode = None
        self.__lastCodeTimestamp = None
    
    def handleCode(self, code):
        if (((self.__lastCode == None) and (self.__lastCodeTimestamp == None)) or (code != self.__lastCode) or ((code == self.__lastCode) and ((self.__lastCodeTimestamp + datetime.timedelta(seconds=2)) < datetime.datetime.utcnow()))):
            self.__lastCode = code
            self.__lastCodeTimestamp = datetime.datetime.utcnow()
            try:
                dbSession = app.db.session
                dbSession.add(RFSniffer(code))
                dbSession.commit()
            except:
                dbSession.rollback()
                raise