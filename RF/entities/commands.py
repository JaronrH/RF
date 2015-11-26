from sqlalchemy import Column, String, Sequence, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from entities import *

class Command(Base):
    'Command Record'
    __tablename__ = "commands"
    
    id = Column(Integer, Sequence("record_seq"), primary_key=True)
    name = Column("name", String(50), index=True, nullable=False)
    style = Column("style", String(50), nullable=False)
    codes = relationship('Code', cascade="all, delete-orphan", backref="command")
    button_id = Column('button_id', Integer, ForeignKey('buttons.id'))
    UniqueConstraint('button_id', 'name', name='unique_button_command')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<command(id='%s', name='%s')>" % (self.id, self.name)