from flask.ext.classy import FlaskView, route
from components import featureBroker
from flask import render_template, request, abort, redirect, flash, url_for
from datetime import datetime, timedelta
import json
import drivers.rf
import random
import app
from entities import *
from time import sleep

class ManageController(FlaskView):
    route_base = '/manage/'
    interface = featureBroker.RequiredFeature('entityInterfaces', featureBroker.HasMethods('getCodes', 'getButton', 'removeButton', 'addButton'))
    autolightConfig = featureBroker.RequiredFeature('conf_AutoLight')

    @route('/')
    def index(self):
        """Management Page."""
        
        return render_template(
            'manage.html',
            title='Manage',
            year=datetime.datetime.now().year
        )
        
    @route('/buttons/remote_add', methods=['POST'])
    def addremoteButton(self):
        '''Create a new Button from incoming remote signal'''
        try:
            now = datetime.datetime.utcnow()
            timeLimit = now + timedelta(seconds=10)
            code = None
            while ((code == None) and (datetime.datetime.utcnow() <= timeLimit)):
                for record in app.db.session.query(RFSniffer).filter(RFSniffer.date_created >= now).order_by(RFSniffer.date_created):
                    code = record.code
                    break;
                sleep(1/4.)
            if (code == None):
                return abort(408)
            codes = drivers.rf.analyseCode(code)
            data = request.get_json(force=True)
            button = self.interface.addButton(data['name'], **data)
            button.save()
            button.addCommand("On", style = "success", codes = [codes['on']])
            button.addCommand("Off", style = "danger", codes = [codes['off']])
            button.save()
            return json.dumps({'id': button.id})
        except:
            return abort(400)

    @route('/buttons/add', methods=['POST'])
    def addButton(self):
        '''Create a new Button'''
        try:
            data = request.get_json(force=True)
            button = self.interface.addButton(data['name'], **data)
            button.save()
            code = None
            allCodes = self.interface.getCodes() 
            while (True): 
            	code = random.randint(10000, 9999999)
                for c in allCodes:
                    if c == code:
                        code = None
                        break
                if code != None:
                    break 
            codes = drivers.rf.analyseCode(code)
            button.addCommand("On", style = "success", codes = [codes['on']])
            button.addCommand("Off", style = "danger", codes = [codes['off']])
            button.save()
            return json.dumps({'id': button.id})
        except:
            return abort(400)
    
    @route('/buttons/<button_id>/remove', methods=['POST'])
    def removeButton(self, button_id):
        '''Remove a Button'''
        try:
            self.interface.removeButton(id=int(button_id))
            return "{}", 200
        except:
            return abort(400)
    
    @route('/buttons/<button_id>/hide', methods=['POST'])
    def hideButton(self, button_id):
        '''Hide a Button'''
        try:
            button = self.interface.getButton(id=int(button_id))
            button.visible = False
            button.save()
            return "{}", 200
        except:
            return abort(400)
    
    @route('/buttons/<button_id>/show', methods=['POST'])
    def showButton(self, button_id):
        '''Show a Button'''
        try:
            button = self.interface.getButton(id=int(button_id))
            button.visible = True
            button.save()
            return "{}", 200
        except:
            return abort(400)
        
    @route('/buttons/<button_id>/rename', methods=['POST'])
    def renameButton(self, button_id):
        '''Rename a Button'''
        try:
            button = self.interface.getButton(id=int(button_id))
            data = request.get_json(force=True)
            button.name = data['name']
            button.save()
            return "{}", 200
        except:
            return abort(400)

    @route('/buttons/<button_id>/updateIcon', methods=['POST'])
    def updateIcon(self, button_id):
        '''Change the icon of a Button'''
        try:
            button = self.interface.getButton(id=int(button_id))
            data = request.get_json(force=True)
            button.icon = data['icon']
            button.save()
            return "{}", 200
        except:
            return abort(400)

    @route('/buttons/<button_id>/edit')
    def edit(self, button_id):
        """Edit Button Page."""
        
        button = self.interface.getButton(id=int(button_id))
        if (button == None):
            flash('Unable to find button with the id of '+button_id+'.', 'error')
            return redirect(url_for('ManageController:index'))
        return render_template(
                'edit.html',
                title=button.name,
                button=button,
                autolightConfig=self.autolightConfig,
                year=datetime.datetime.now().year
            )

    @route('/buttons/<button_id>/command/add', methods=["POST"])
    def addCommand(self, button_id):
        '''Add a new command to a Button'''
        try:
            button = self.interface.getButton(id=int(button_id))
            data = request.get_json(force=True)
            button.addCommand(data['name'], style = "primary")
            button.save()
            return "{}", 200
        except: 
            return abort(400)

    @route('/buttons/<button_id>/command/<command_id>/remove', methods=["POST"])
    def removeCommand(self, button_id, command_id):
        '''Remove a command'''
        try:
            button = self.interface.getButton(id=int(button_id))
            button.removeCommand(id=int(command_id))
            button.save()
            return "{}", 200
        except:
            return abort(400)

    @route('/buttons/<button_id>/command/<command_id>/rename', methods=["POST"])
    def renameCommand(self, button_id, command_id):
        '''Rename a command'''
        try:
            command = self.interface.getCommand(command_id=int(command_id))
            data = request.get_json(force=True)
            command.name = data['name']
            command.save()
            return "{}", 200
        except:
            return abort(400)

    @route('/buttons/<button_id>/command/<command_id>/style', methods=["POST"])
    def styleCommand(self, button_id, command_id):
        '''Rename a command'''
        try:
            command = self.interface.getCommand(command_id=int(command_id))
            data = request.get_json(force=True)
            command.style = data['style']
            command.save()
            return "{}", 200
        except:
            return abort(400)

    @route('/buttons/<button_id>/command/<command_id>/autolight/enable/set', methods=["POST"])
    def setAutolightEnableCommand(self, button_id, command_id):
        '''Set Autolight Enable Command'''
        try:
            command = self.interface.getCommand(command_id=int(command_id))
            command.setAsAutoLightEnable()
            command.save()
            return "{}", 200
        except:
            return abort(400)

    @route('/buttons/<button_id>/command/<command_id>/autolight/disable/set', methods=["POST"])
    def setAutolightdisableCommand(self, button_id, command_id):
        '''Set Autolight disable Command'''
        try:
            command = self.interface.getCommand(command_id=int(command_id))
            command.setAsAutoLightDisable()
            command.save()
            return "{}", 200
        except:
            return abort(400)

    @route('/buttons/<button_id>/command/<command_id>/autolight/enable/remove', methods=["POST"])
    def removeAutolightEnableCommand(self, button_id, command_id):
        '''Remove Autolight Enable Command'''
        try:
            button = self.interface.getButton(id=int(button_id))
            if (button.autolight['enable'].id != int(command_id)):
                return abort(400)
            button.clearAutoLightEnable()
            button.save()
            return "{}", 200
        except:
            return abort(400)

    @route('/buttons/<button_id>/command/<command_id>/autolight/disable/remove', methods=["POST"])
    def removeAutolightDisableCommand(self, button_id, command_id):
        '''Remove Autolight disable Command'''
        try:
            button = self.interface.getButton(id=int(button_id))
            if (button.autolight['disable'].id != int(command_id)):
                return abort(400)
            button.clearAutoLightDisable()
            button.save()
            return "{}", 200
        except:
            return abort(400)

    @route('/buttons/<button_id>/command/<command_id>/code/add', methods=["POST"])
    def addCode(self, button_id, command_id):
        '''Add a new code to a command'''
        try:
            command = self.interface.getCommand(command_id=int(command_id))
            data = request.get_json(force=True)
            command.addCode(int(data['code']))
            command.save()
            return "{}", 200
        except:
            return abort(400)

    @route('/buttons/<button_id>/command/<command_id>/code/<code>/remove', methods=["POST"])
    def removeCode(self, button_id, command_id, code):
        '''Add a new code to a command'''
        try:
            command = self.interface.getCommand(command_id=int(command_id))
            command.removeCode(code=int(code))
            command.save()
            return "{}", 200
        except:
            return abort(400)

featureBroker.features.Provide('controller', ManageController)