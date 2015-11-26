import pkgutil
import inspect
from components import featureBroker

__all__ = []

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if name.startswith('__'):
            continue

        globals()[name] = value
        __all__.append(name)

class Commander(featureBroker.Component):
    commands = featureBroker.RequiredFeatures('command', featureBroker.HasMethods('runCommand'))

    def runCommand(self, command):
        """ Run a given command. """
        for c in self.commands:
            c.runCommand(command)

featureBroker.features.Provide('commander', Commander)