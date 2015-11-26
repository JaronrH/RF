from sqlalchemy import Column, Sequence, Integer, ForeignKey
from entities import *

class Code(Base):
    'Code associated with a command'
    __tablename__ = "codes"
    id = Column(Integer, Sequence("record_seq"), primary_key=True)
    code = Column("name", Integer, nullable=False)
    command_id = Column(Integer, ForeignKey('commands.id'))

    def __init__(self, code):
        self.code = code
    
    def __repr__(self):
        return "<code(id='%s', code='%s')>" % (self.id, self.code)