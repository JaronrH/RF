from flask.ext.classy import FlaskView, route
from components import featureBroker
from flask import render_template, request
from datetime import datetime

class ScheduleController(FlaskView):
    route_base = '/schedule/'
    interface = featureBroker.RequiredFeature('entityInterfaces', featureBroker.HasMethods('getCommand'))
    scheduledCommands = featureBroker.RequiredFeature('scheduledCommands', featureBroker.HasMethods('scheduleSingleCommand'))

    @route('/button/<button_ref>/<command_ref>', methods = ['POST'])
    def scheduleCommand(self, button_ref, command_ref):
        """Processes a button request."""
        
        # Get Command
        command = self.interface.getCommand(button_name=button_ref, command_name=command_ref)
        if (command == None):
            try:
                command = self.interface.getCommand(button_id=int(button_ref), command_name=command_ref)
            except:
                command = None
        if (command == None):
            try:
                command = self.interface.getCommand(button_id=int(button_ref), command_id=int(command_ref))
            except:
                command = None
        if (command == None):
            try:
                command = self.interface.getCommand(button_name=button_ref, command_id=int(command_ref))
            except:
                command = None
        if (command == None):
            return abort(400)

        # Get JSON data from post
        jsonData = request.get_json(force=True)
            
        # Get Hours/Min from time in body
        time = jsonData['time'].split(':')
        if (len(time) != 2):
            return abort(400)
        hour = time[0]
        min = time[1]
        
        # Schedule Command
        self.scheduledCommands.scheduleSingleCommand(command, 'cron', jsonData['deleteWhenDone'], hour=hour, minute=min)
        return "{}", 200

featureBroker.features.Provide('controller', ScheduleController)