from components import featureBroker
from drivers.rf import send
import os

class rf433(featureBroker.Component):
    def runCommand(self, command):
        """ Run a given command. """
        if len(command.codes) > 0:
            if os.name == 'nt':
                print 'Codesend would send: {commands}'.format(commands=str(command.codes).translate(None, "'"))
            else:
                send(command.codes)

featureBroker.features.Provide('command', rf433)