import app.application
import sys

####################################################
#  Go To app/application.py for actual program logic!
####################################################

if __name__ == "__main__":
    PIDFILE = '/tmp/RF.pid'

    def getPid():
        try:
            pf = file(PIDFILE,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        except SystemExit:
            pid = None
        return pid

    daemon = app.application.ApplicationDaemon(PIDFILE)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            pid = getPid()
            if pid:
                print('Daemon is running as pid '+str(pid))
            else:
                print('Daemon is not running.')
        elif 'console' == sys.argv[1]:
            if (getPid() == None):
                app = app.application.Application()
                app.run()
            else:
                print('Application already running as Daemon')
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: "+sys.argv[0]+" start|stop|restart|console|status")
        sys.exit(2)