from entities import *
from components import featureBroker
from components.properties import property
from sqlalchemy import inspect
import app

class CommandInterface(object):
    def __init__(self, *args, **kwargs):
        if 'entity' in kwargs:
            self._entity = kwargs['entity']
            if self._entity == None:
                raise ValueError("Entity cannot be defined as None.")
        elif (len(args) == 0):
            raise ValueError("Must specify a Name")
        else:
            self._entity = Command(args[0])
            if 'style' in kwargs:
                self.style = kwargs['style']
            else:
                self.style = "primary"
            if 'codes' in kwargs:
                for c in kwargs['codes']:
                    self.addCode(c)
    
    @property
    def id():
        '''ID'''
        def fget(self):
            return self._entity.id
    
    @property
    def name():
        '''Name'''
        def fget(self):
            return self._entity.name
        def fset(self, value):
            self._entity.name = value
            
    @property
    def style():
        '''Style'''
        def fget(self):
            return self._entity.style
        def fset(self, value):
            self._entity.style = value
            
    @property
    def codes():
        '''Codes'''
        def fget(self):
            codes = []
            for c in self._entity.codes:
                codes.append(c.code)
            return codes
    
    def addCode(self, code):
        '''Create and add a new Code'''
        self._entity.codes.append(Code(code))
    
    def removeCode(self, *args, **kwargs):
        '''Remove an existing Code by {id} or {code}'''
        if 'id' in kwargs:
            for c in self._entity.codes:
                if c.id == kwargs['id']:
                    self._entity.codes.remove(c)
                    break
        elif 'code' in kwargs:
            for c in self._entity.codes:
                if c.code == kwargs['code']:
                    self._entity.codes.remove(c)
                    break
        
    def setAsAutoLightEnable(self):
        '''Set this command as the AutoLight Enable command'''
        if self._entity.id == None:
            raise ValueError("Cannot set command as AutoLight Enable: Button backref not populated.")
        self._entity.button.autolight.enable_command = self._entity
    
    def setAsAutoLightDisable(self):
        '''Set this command as the AutoLight Disable command'''
        if self._entity.id == None:
            raise ValueError("Cannot set command as AutoLight Disable: Button backref not populated.")
        self._entity.button.autolight.disable_command = self._entity
    
            
    @property
    def button():
        '''Parent Button'''
        def fget(self):
            if self._entity.button == None:
                raise ValueError("Cannot get Button property: Button backref not populated.")
            return self._entity.button
            
    def save(self):
        dbSession = None
        try:
            dbSession = inspect(self._entity).session;
            if dbSession == None:
                dbSession = app.db.session
            if (self._entity.id == None):
                dbSession.add(self._entity)
            dbSession.commit()
        except:
            dbSession.rollback()
            raise

class ButtonInterface(object):
    def __init__(self, *args, **kwargs):
        if 'entity' in kwargs:
            self._entity = kwargs['entity']
            if self._entity == None:
                raise ValueError("Entity cannot be defined as None.")
        elif (len(args) == 0):
            raise ValueError("Must specify a Name")
        else:
            self._entity = Button(args[0])
            if 'visible' in kwargs:
                self.visible = kwargs['visible']
            else:
                self.visible = True
            if 'icon' in kwargs:
                self.icon = kwargs['icon']
            else:
                self.icon = "fa fa-lightbulb-o"
    
    @property
    def id():
        '''ID'''
        def fget(self):
            return self._entity.id
    
    @property
    def visible():
        '''Is this command visible in the UI?'''
        def fget(self):
            return self._entity.visible
        def fset(self, value):
            self._entity.visible = value
            
    @property
    def name():
        '''Name'''
        def fget(self):
            return self._entity.name
        def fset(self, value):
            self._entity.name = value
            
    @property
    def icon():
        '''Icon CSS'''
        def fget(self):
            return self._entity.icon
        def fset(self, value):
            self._entity.icon = value
            
    @property
    def autolight():
        '''AutoLight'''
        def fget(self):
            results = {}
            if (self._entity.autolight.enable_command != None):
                results['enable'] = CommandInterface(entity = self._entity.autolight.enable_command)
            if (self._entity.autolight.disable_command != None):
                results['disable'] = CommandInterface(entity = self._entity.autolight.disable_command)
            return results
    
    def clearAutoLightEnable(self):
        '''Remove any AutoLight Enable command'''
        self._entity.autolight.enable_command = None
    
    def clearAutoLightDisable(self):
        '''Remove any AutoLight Disable command'''
        self._entity.autolight.disable_command = None
        
    @property
    def commands():
        '''Commands'''
        def fget(self):
            commands = []
            for c in self._entity.commands:
                commands.append(CommandInterface(entity = c))
            return commands
        
    def addCommand(self, *args, **kwargs):
        '''Add an existing command'''
        command = CommandInterface(*args, **kwargs)
        self._entity.commands.append(command._entity)
        return command
    
    def removeCommand(self, *args, **kwargs):
        '''Remove an existing Command by {id} or {name}'''
        if 'id' in kwargs:
            for c in self._entity.commands:
                if c.id == kwargs['id']:
                    if (self._entity.autolight.enable_command != None) and (self._entity.autolight.enable_command.id == c.id):
                        self._entity.autolight.enable_command = None
                    if (self._entity.autolight.disable_command != None) and (self._entity.autolight.disable_command.id == c.id):
                        self._entity.autolight.disable_command = None
                    self._entity.commands.remove(c)
                    break
        elif 'name' in kwargs:
            for c in self._entity.commands:
                if c.name == kwargs['name']:
                    if (self._entity.autolight.enable_command != None) and (self._entity.autolight.enable_command.id == c.id):
                        self._entity.autolight.enable_command = None
                    if (self._entity.autolight.disable_command != None) and (self._entity.autolight.disable_command.id == c.id):
                        self._entity.autolight.disable_command = None
                    self._entity.commands.remove(c)
                    break
                    
    def getCommand(self, *args, **kwargs):
        '''Get an existing command by {id} or {name}'''
        if 'id' in kwargs:
            for c in self._entity.commands:
                if c.id == kwargs['id']:
                    return CommandInterface(entity=c)
            return None
        elif 'name' in kwargs:
            for c in self._entity.commands:
                if c.name == kwargs['name']:
                    return CommandInterface(entity=c)
            return None
        else:
            raise ValueError("Must use getCommand with an {id} or {name] to look up.")
            
    def save(self):
        dbSession = None
        try:
            dbSession = inspect(self._entity).session;
            if dbSession == None:
                dbSession = app.db.session
            if (self._entity.id == None):
                dbSession.add(self._entity)
            dbSession.commit()
        except:
            dbSession.rollback()
            raise

class EntityInterfaces(featureBroker.Component):
    def addButton(self, *args, **kwargs):
        '''Create a new Button interface'''
        return ButtonInterface(*args, **kwargs)
    
    def getButtons(self):
        '''Get all the available buttons'''
        dbSession = app.db.session
        buttons = []
        for b in dbSession.query(Button):
            buttons.append(ButtonInterface(entity = b))
        return buttons
    
    def removeButton(self, *args, **kwargs):
        '''Remove an existing button by {id} or {name}'''
        dbSession = None
        try:
            dbSession = app.db.session
            button = None
            if 'id' in kwargs:
                button = dbSession.query(Button).filter(Button.id == kwargs['id']).one()
            elif 'name' in kwargs:
                button = dbSession.query(Button).filter(Button.name == kwargs['name']).one()
            else:
                raise ValueError("Must use getButton with an {id} or {name] to look up.")
            
            if (button != None):
                dbSession.delete(button)
                dbSession.commit()
        except:
            dbSession.rollback()
            raise
    
    def getButton(self, *args, **kwargs):
        '''Get an existing button by {id} or {name}'''
        dbSession = app.db.session
        if 'id' in kwargs:
            try:
                return ButtonInterface(entity=dbSession.query(Button).filter(Button.id == kwargs['id']).one())
            except:
                return None
        elif 'name' in kwargs:
            try:
                return ButtonInterface(entity=dbSession.query(Button).filter(Button.name == kwargs['name']).one())
            except:
                return None
        else:
            raise ValueError("Must use getButton with an {id} or {name] to look up.")
    
    def getCommand(self, *args, **kwargs):
        '''Get an existing command by combination of {button_id}/{button_name} and {command_id}/{command_name}'''
        if 'command_id' in kwargs:
            dbSession = app.db.session
            return CommandInterface(entity=dbSession.query(Command).filter(Command.id == kwargs['command_id']).one())
        
        button = None
        if 'button_id' in kwargs:
            button = self.getButton(id = kwargs['button_id'])
        elif 'button_name' in kwargs:
            button = self.getButton(name = kwargs['button_name'])
        else:
            raise ValueError("Must use getCommand with an {button_id} or {button_name] to look up.")
        
        if (button == None):
            return None
        
        if 'command_name' in kwargs:
            return button.getCommand(name = kwargs['command_name'])
        else:
            raise ValueError("Must use getCommand with an {command_id} or {command_name] to look up.")
    
    def getCodes(self):
        '''Get all the codes that are in use'''
        dbSession = app.db.session
        codes = []
        for c in dbSession.query(Code):
            codes.append(c.code)
        return codes

    def lookupCode(self, code):
        '''Lookup a code to see how it is ued in the system'''
        dbSession = app.db.session
        results = []
        for c in dbSession.query(Code).filter(Code.code == code):
            results.append({
                    'code': int(code),
                    'button': ButtonInterface(entity=c.command.button),
                    'command': CommandInterface(entity=c.command)
                })
        return results

featureBroker.features.Provide('entityInterfaces', EntityInterfaces)