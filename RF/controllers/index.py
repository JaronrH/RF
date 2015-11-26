from flask.ext.classy import FlaskView, route
from components import featureBroker
from flask import render_template, request, send_from_directory, abort
from datetime import datetime
import os
import controllers
import json
import app
import drivers.rf

class IndexController(FlaskView):
    interface = featureBroker.RequiredFeature('entityInterfaces', featureBroker.HasMethods('getCommand', 'getButtons'))
    commander =  featureBroker.RequiredFeature('commander', featureBroker.HasMethods('runCommand'))
    route_base = '/'

    @route('/favicon.ico')
    def favicon(self):
        return send_from_directory(os.path.join(app.web.root_path, 'static', 'images'),
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @route('/')
    def index(self):
        """Renders the home page."""

        return render_template(
            'index.html',
            title='Power',
            buttons=self.interface.getButtons(),
            year=datetime.now().year
        )

    @route('/code/<code>/send', methods = ['POST'])
    def codeSend(self, code):
        """Send a command."""
        drivers.rf.send([int(code)])
        return "{}", 200

    @route('/button/<button_ref>/<command_ref>', methods = ['POST'])
    def button(self, button_ref, command_ref):
        """Processes a button request."""
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

        # Find Code
        self.commander.runCommand(command)
        return "{}", 200

featureBroker.features.Provide('controller', IndexController)