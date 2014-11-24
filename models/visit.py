"""
This is the sqlalchemy class for communicating with the visits table

"""

from datetime import datetime
from sqlalchemy import Column, Integer, Unicode, DateTime, ForeignKey
import base

class Visit(base.Base):
    """Sqlalchemy deals model"""
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True)
    checkin = Column('checkin', DateTime)
    checkout = Column('checkout', DateTime)
    family_id = Column('family', Integer, ForeignKey('customerfamily.id'))

    def setStatus(self, status, family_id, id=None):
    	self.family_id = family_id
    	if (status == 'checkin'):
    		self.checkin = datetime.now()