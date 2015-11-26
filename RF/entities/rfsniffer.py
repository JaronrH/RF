from sqlalchemy import Column, DateTime, Integer, Sequence
import datetime
import entities

class RFSniffer(entities.Base):
    'RF Sniffer Log'
    __tablename__ = "rf_sniffer"
    
    id = Column(Integer, Sequence("record_seq"), primary_key=True)
    date_created = Column("date_created", DateTime, default=datetime.datetime.utcnow, index=True)
    code = Column('code', Integer, nullable=False)
    
    def __init__(self, code):
        self.code = code
        
    def __repr__(self):
        return "<rf_sniffer(id='%s', code='%s' date='%s')>" % (self.id, self.code, self.date)