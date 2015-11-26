import pkgutil
import inspect
import datetime
import os

__all__ = []

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if name.startswith('__'):
            continue

        globals()[name] = value
        __all__.append(name)

class Formatter(object):
    @staticmethod
    def WinOrLinux(winStr, linStr):
        if os.name == 'nt':
            return winStr
        else:
            return linStr

    @staticmethod
    def day(d):
        return Formatter.utc_to_local(d).strftime(Formatter.WinOrLinux('%b %d, %Y','%b %e, %Y'))

    @staticmethod
    def date(d):
        return Formatter.utc_to_local(d).strftime(Formatter.WinOrLinux('%b %d, %Y, %I:%M:%S %p', '%b %e, %Y, %l:%M:%S %p'))

    @staticmethod
    def utc_to_local(utc):
        offset = datetime.utcnow() - datetime.now()
        return utc - offset

    @staticmethod
    def normalize(str):
        if (str == None):
            return '[n/a]'
        elif (len(str) == 0):
            return '[blank]'
        else:
            return str