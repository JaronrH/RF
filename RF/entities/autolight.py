from sqlalchemy import Column, Sequence, Integer, ForeignKey
from sqlalchemy.orm import relationship
from entities import *

class AutoLight(Base):
    'Autolight Entry.'
    __tablename__ = "autolight"
    
    id = Column(Integer, Sequence("record_seq"), primary_key=True)
    buttons_id = Column(Integer, ForeignKey('buttons.id'), nullable=False)
    enable_command_id = Column(Integer, ForeignKey('commands.id'), nullable=True)
    enable_command = relationship("Command", uselist=False, foreign_keys=[enable_command_id])
    disable_command_id = Column(Integer, ForeignKey('commands.id'), nullable=True)
    disable_command = relationship("Command", uselist=False, foreign_keys=[disable_command_id])

    def __repr__(self):
        return "<autolight(id='%s')>" % (self.id)