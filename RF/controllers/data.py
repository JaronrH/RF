from flask.ext.classy import FlaskView, route
from components import featureBroker
from flask import render_template, request
from datetime import datetime
from flask import render_template
import json

class DataController(FlaskView):
    route_base = '/data/'
    interface = featureBroker.RequiredFeature('entityInterfaces', featureBroker.HasMethods('getCommand'))
    
    @route('/button/<button_ref>/command/<command_ref>')
    def command(self, button_ref, command_ref):
        """Processes a command  request."""
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
        
        return json.dumps({
                'id': command.id,
                'name': command.name,
                'style': command.style,
                'codes': command.codes,
            })

    @route('/button/<button_ref>')
    def button(self, button_ref):
        """Processes a button request."""
        def processCommand(command):
            if (command == None):
                return None
            return {
                'id': command.id,
                'name': command.name,
                'style': command.style,
                'codes': command.codes,
            }
        
        def processCommands(commandList):
            commands = []
            for c in commandList:
                commands.append(processCommand(c))
            return commands
        
        b  = self.interface.getButton(id=button_ref)
        if b == None:
            b = self.interface.getButton(name=button_ref)
        if b == None:
            return abort(400)
        
        return json.dumps({
                'id': b.id,
                'name': b.name,
                'icon': b.icon,
                'visible': b.visible,
                'autolight': {
                    'enable': processCommand(b.autolight['enable']) if 'enable' in b.autolight else None,
                    'disable': processCommand(b.autolight['disable']) if 'disable' in b.autolight else None
                },
                'commands': processCommands(b.commands)
            })

    @route('/buttons')
    def buttons(self):
        """Get Buttons Details"""
        
        def processCommand(command):
            if (command == None):
                return None
            return {
                'id': command.id,
                'name': command.name,
                'style': command.style,
                'codes': command.codes,
            }
        
        def processCommands(commandList):
            commands = []
            for c in commandList:
                commands.append(processCommand(c))
            return commands
        
        results = []
        for b in self.interface.getButtons():
            results.append({
                'id': b.id,
                'name': b.name,
                'icon': b.icon,
                'visible': b.visible,
                'autolight': {
                    'enable': processCommand(b.autolight['enable']) if 'enable' in b.autolight else None,
                    'disable': processCommand(b.autolight['disable']) if 'disable' in b.autolight else None
                },
                'commands': processCommands(b.commands)
            })
        
        return json.dumps(results)

    @route('/lookup/code/<code>')
    def lookupCode(self, code):
        def processCommand(command):
            if (command == None):
                return None
            return {
                'id': command.id,
                'name': command.name,
                'style': command.style,
                'codes': command.codes,
            }
        
        def processCommands(commandList):
            commands = []
            for c in commandList:
                commands.append(processCommand(c))
            return commands
        
        results = []
        for c in self.interface.lookupCode(code):
            results.append({
                'button': {
                        'id': c['button'].id,
                        'name': c['button'].name,
                        'icon': c['button'].icon,
                        'visible': c['button'].visible,
                        'autolight': {
                            'enable': processCommand(c['button'].autolight['enable']) if 'enable' in c['button'].autolight else None,
                            'disable': processCommand(c['button'].autolight['disable']) if 'disable' in c['button'].autolight else None
                        },
                        'commands': processCommands(c['button'].commands)
                    },
                'command': processCommand(c['command'])
            })
        
        return json.dumps(results)

featureBroker.features.Provide('controller', DataController)