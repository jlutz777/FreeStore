"""
This is the sqlalchemy class for communicating with the visits table

"""

from sqlalchemy import Column, Integer, Unicode, DateTime, ForeignKey
import base

class Visit(base.Base):
    """Sqlalchemy deals model"""
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True)
    checkin = Column('checkin', DateTime)
    checkout = Column('checkout', DateTime)
    family_id = Column('family', Integer, ForeignKey('customerfamily.id'))
