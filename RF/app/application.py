from components import featureBroker
from commands import *
import sys
import time
from components.daemon import Daemon
import os
import json
import logging.config
from ConfigParser import SafeConfigParser
from flask import Flask
from controllers import *
import app
from schedules import *
import schedules
from flask_apscheduler import APScheduler
import components.entityInterfaces
import components.ScheduledCommands
from flask_sqlalchemy import SQLAlchemy
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.memory import MemoryJobStore
import entities
from entities import *
from components.rfSniffer import rfSniffer

class Application(object):
    def run(self, isDaemon = False):
        ####################################################
        #  Setup Logging
        ####################################################
        self.setup_logging()

        ####################################################
        #  Setup Configuration
        ####################################################
        parser = SafeConfigParser()
        parser.read('RF.conf')
        for section_name in parser.sections():
            featureBroker.features.Provide('conf_{name}'.format(name=section_name), dict(parser.items(section_name)))
        
        ####################################################
        #  Start Flask
        ####################################################

        app.web = Flask("__main__")

        # Create Scheduler
        if not app.web.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            app.web.config['SCHEDULER_VIEWS_ENABLED']=True
            app.web.config['SCHEDULER_JOBSTORES']={
                    'default': MemoryJobStore(),
                    'db': SQLAlchemyJobStore(url='sqlite:///'+featureBroker.RequiredFeature('conf_DB').result['jobs'])
                }
            scheduler = APScheduler()
            jobs = featureBroker.RequiredFeatures('job', featureBroker.HasMethods('register')).result
            for job in jobs:
                job.register(scheduler.scheduler)
            scheduler.init_app(app.web)
            scheduler.start()
            featureBroker.features.Provide('scheduler', scheduler.scheduler)
        
        # Register Controllers
        controllers = featureBroker.RequiredFeatures('controller', featureBroker.HasMethods('register')).result
        for controller in controllers:
            controller.register(app.web)

        # Set secret Key
        app.web.secret_key = 'A0ew:DE~7/T6yA^8vqNgjVB5tZr98j/3yX R~XHH!jmew:DE~7/T6yA^8vqNgjVB5tN]LWX/,?RT'

        # Flask-SQLAlchemy
        app.web.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+featureBroker.RequiredFeature('conf_DB').result['rf']
        app.db = SQLAlchemy(app.web)
        entities.Base.metadata.create_all(app.db.engine, checkfirst=True)
        
        # RF Sniffer
        if not app.web.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            sniffer = rfSniffer()
        
        app.web.run(host='0.0.0.0', port=parser.getint("Web", "port"), debug=(not isDaemon))

    def setup_logging(self,
        default_path='app/loggingConfig.json', 
        default_level=logging.INFO,
    ):
        """Setup logging configuration"""
        path = default_path
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)

class ApplicationDaemon(Daemon):
    def run(self):
        # Or simply merge your code with MyDaemon.
        app = Application()
        app.run(True)