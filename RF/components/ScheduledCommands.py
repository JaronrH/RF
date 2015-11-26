from components import featureBroker
import urllib2
import drivers.ipaddress
import json
import datetime
import logging
import random

class ScheduledCommands(featureBroker.Component):
    scheduler = featureBroker.RequiredFeature('scheduler')

    def __init__(self, *args, **kwargs):
        return super(ScheduledCommands, self).__init__(*args, **kwargs)
    
    def scheduleSingleCommand(self, command, jobType, deleteWhenDone, **kwargs):
        kwargs['jobstore'] = 'db';
        kwargs['id'] = "["+str(random.randint(0, 99999999999))+"]Button '"+command.button.name+"' (ID: "+str(command.button.id)+"); Command '"+command.name+"' (ID: "+str(command.id)+")";
        kwargs['args'] = (kwargs['id'], command.id, deleteWhenDone);
        self.scheduler.add_job(runCommand, jobType, **kwargs)

def runCommand(jobId, commandId, deleteWhenDone):
    # Load Necessary Components
    interface = featureBroker.RequiredFeature('entityInterfaces', featureBroker.HasMethods('getCommand')).result
    commander =  featureBroker.RequiredFeature('commander', featureBroker.HasMethods('runCommand')).result
    
    # Find command and run it
    command = interface.getCommand(command_id = commandId)
    if (command != None):
        commander.runCommand(command)
    
    # Delete when done?
    if (deleteWhenDone):
        scheduler = featureBroker.RequiredFeature('scheduler').result
        scheduler.remove_job(jobId)
    

featureBroker.features.Provide('scheduledCommands', ScheduledCommands)