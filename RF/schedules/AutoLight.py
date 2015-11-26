from components import featureBroker
import urllib2
import drivers.ipaddress
import json
import datetime
import logging

class AutoLight(featureBroker.Component):
    interface = featureBroker.RequiredFeature('entityInterfaces', featureBroker.HasMethods('getButtons'))
    config = featureBroker.RequiredFeature('conf_AutoLight')
    commander =  featureBroker.RequiredFeature('commander', featureBroker.HasMethods('runCommand'))

    def __init__(self, *args, **kwargs):
        self.triggered = False
        self._jobName = 'AutoLight'
        self._scheduler = None
        self.triggered = False
        self.log = logging.getLogger('AutoLight')
        return super(AutoLight, self).__init__(*args, **kwargs)
    
    def disabler(self):
        self.log.info("AutoLight is being disabled")
        self._scheduler.pause_job(self._jobName+' Checker')
        if self.triggered:
            self.runCommands('disable')
    
    def enabler(self):
        self.log.info("AutoLight is being enabled")
        self.triggered = False;
        self._scheduler.resume_job(self._jobName+' Checker')
        self.checkLight()
    
    def register(self, scheduler):
        self._scheduler = scheduler
        
        # Schedule jobs
        self._scheduler.add_job(self.enabler, 'cron', id=self._jobName+' Enabler', hour=int(self.config['enablehour']), minute=int(self.config['enablemin']), max_instances=1)
        self._scheduler.add_job(self.disabler, 'cron', id=self._jobName+' Disabler', hour=int(self.config['disablehour']), minute=int(self.config['disablemin']), max_instances=1)
        self._scheduler.add_job(self.checkLight, 'interval', id=self._jobName+' Checker', minutes=1, next_run_time=None, max_instances=1)

    def checkLight(self):
        try:
            # Get Lux Value
            lux = self.getLux()
            
            # Check Lighting
            if ((lux != None) and (lux < int(self.config['luxlimit']))):
                self.log.info('AutoLight is in Valid Range (Lux = {lux}).'.format(lux=lux))
                self.triggered = True
                self._scheduler.pause_job(self._jobName+' Checker')
                self.runCommands('enable')

        except Exception, e:
            self.log.exception(e)

    def runCommands(self, command):
        # Run command if needed
        for button in self.interface.getButtons():
            if command in button.autolight:
                try:
                    self.log.info('Sending "{c}" to {name}.'.format(c=button.autolight[command].name, t=command, name=button.name))
                    self.commander.runCommand(button.autolight[command])
                except Exception, e:
                    self.log.exception(e)
            
    def getLux(self):
        try:
            # Get Sensor Data
            ip = None
            if 'address' in self.config:
                ip = self.config['address']
            else:
                ip = drivers.ipaddress.getIpAddress()
            url = 'http://'+ip+':'+self.config['port']+self.config['path'];
            self.log.debug('Lux Posting URL: {url}'.format(url=url))
            sensorData = json.loads(urllib2.urlopen(url).read())

            # Get LUX value
            for sensor in sensorData['sensors']:
                if (sensor['name'] == self.config['sensorname']):
                    self.log.debug('Value for "{sensor}" sensor: {value}'.format(sensor=self.config['sensorname'], value=sensor['value']))
                    return sensor['value']

            # Could not get value
            return None
        except Exception, e:
            self.log.exception(e)
            return None

featureBroker.features.Provide('job', AutoLight)