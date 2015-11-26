from sqlalchemy import Column, String, Sequence, Integer, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from entities import *

class Button(Base):
    'Emulate a "Button" row from the remote.'
    __tablename__ = "buttons"
    
    id = Column(Integer, Sequence("record_seq"), primary_key=True)
    name = Column("name", String(50), index=True, nullable=False, unique=True)
    visible = Column("visible", Boolean, nullable=False)
    icon = Column("icon", String(50), nullable=False)
    commands = relationship('Command', cascade="all, delete-orphan", backref="button")
    autolight = relationship('AutoLight', cascade="all, delete-orphan", uselist=False)

    def __init__(self, name):
        self.name = name
        self.autolight = AutoLight()

    def __repr__(self):
        return "<button(id='%s', name='%s')>" % (self.id, self.name)