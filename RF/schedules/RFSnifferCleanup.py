from components import featureBroker
import datetime
import app
from entities import *
import traceback

class RFSnifferCleanup(featureBroker.Component):
    config = featureBroker.RequiredFeature('conf_RFSniffer')

    def register(self, scheduler):
        scheduler.add_job(self.doCleanup, 'cron', id='RF Sniffer History Cleanup', hour=2, max_instances=1)

    def doCleanup(self):
        cleanupDate = datetime.datetime.utcnow()-datetime.timedelta(days=int(self.config['cleanup_age_days']))
        dbSession = None
        try:
            dbSession = app.db.session;
            dbSession.query(RFSniffer).filter(RFSniffer.date_created < cleanupDate).delete()
            dbSession.commit()
        except:
            dbSession.rollback()
            traceback.print_exc()
            raise

featureBroker.features.Provide('job', RFSnifferCleanup)