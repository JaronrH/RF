# 433 Wireless: https://github.com/ninjablocks/433Utils and https://www.samkear.com/hardware/control-power-outlets-wirelessly-raspberry-pi
# security should be 755 for the required files!

from subprocess import call, Popen, PIPE,STDOUT
import os
import subprocess
import threading
import time
import Queue
import sys

script_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
helperExe = os.path.join(script_path, "codesend")
snifferExe = os.path.join(script_path, "RFSniffer")

class __SendThread(threading.Thread):
    def __init__(self, daemon = True):
        threading.Thread.__init__(self)
        self.daemon = daemon
        self.queue = Queue.Queue()
        self.start()
    
    def sendCode(self, code):
        self.queue.put(code)
    
    def run(self):
        while (True):
            if (self.queue.empty()):
                time.sleep(1/10)
                continue
            if os.name == 'nt':
                print "Emulating Sending code {code}".format(code=self.queue.get())
            else:
                call([helperExe, str(self.queue.get())])
    
class __MonitorThread(threading.Thread):
    __lock = threading.Lock()

    def __init__(self, daemon = True, listeners = [], listenOnce = []):
        threading.Thread.__init__(self)
        self.daemon = daemon
        self.__listeners = listeners
        self.__listenOnce = listenOnce
        if (len(self.__listeners)+len(self.__listenOnce) > 0):
            self.start()
    
    def addListener(self, listener):
        try:
            self.__lock.acquire()
            self.__listeners.append(listener)
        finally:
            self.__lock.release()
        if (not self.is_alive()):
            self.start()
    
    def listenOnce(self, listener):
        try:
            self.__lock.acquire()
            self.__listenOnce.append(listener)
        finally:
            self.__lock.release()
        if (not self.is_alive()):
            self.start()
    
    def run(self):
        proc = None
        if os.name == 'nt':
            proc = Popen([sys.executable, snifferExe+'Mock.py'], stdout = PIPE)
        else:
            proc = Popen([snifferExe], stdout = PIPE)
        for code in iter(proc.stdout.readline, b''):
            try:
                self.__lock.acquire()
                for listener in self.__listeners:
                    try:
                        listener.handleCode(int(code))
                    except:
                        pass;
                for listener in self.__listenOnce:
                    try:
                        listener.handleCode(int(code))
                    except:
                        pass;
                self.__listenOnce = []
            finally:
                self.__lock.release()

class __Listener(object):
    def __init__(self):
        self.code = None

    def handleCode(self, code):
        self.code = code
        
__monitor = None
__sender = None

def send(values):
    global __sender
    if (__sender is None):
       __sender = __SendThread()
    for value in values:
        __sender.sendCode(str(value))

def analyseCode(code):
    if (code% 2 == 0):
	return { 
          'on': code-9,
          'off': code
        }
    else:
	return { 
          'on': code,
          'off': code+9
        }

def getCode():
    global __monitor 
    if (__monitor is None):
       __monitor = __MonitorThread()
    l = __Listener()
    __monitor.listenOnce(l)
    while (l.code == None):
        time.sleep(1/10)
    return l.code

def addCodeListener(listener):
    global __monitor 
    if (__monitor is None):
       __monitor = __MonitorThread()
    __monitor.addListener(listener)
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        send([sys.argv[1]])
    else:            
        print 'Listening for code...'
        results = analyseCode(getCode())
        if (results == None):
            print 'Did not receive a code.'
        else:
            print 'Recieve code: on={on}; off={off}'.format(on=results['on'], off=results['off'])

    
