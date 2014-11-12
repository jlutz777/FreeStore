"""
This is the sqlalchemy class for communicating with the database.

"""

from sqlalchemy import Column, Integer, Sequence, Unicode, DateTime
from sqlalchemy.orm import relationship, backref
import base

class CustomerFamily(base.Base):
    """Sqlalchemy deals model"""
    __tablename__ = "customerfamily"

    id = Column(Integer, primary_key=True)
    email = Column('email', Unicode, info={'label': 'Email'})
    phone = Column('phone', Unicode, default=unicode(''), info={'label': 'Phone'})
    address = Column('address', Unicode, info={'label': 'Street Address'})
    city = Column('city', Unicode, nullable=False, info={'label': 'City'})
    state = Column('state', Unicode, nullable=False, info={'label': 'State'})
    zip = Column('zip', Unicode, nullable=False, info={'label': 'Zip'})
    datecreated = Column('datecreated', DateTime, info={'label': 'Date Created'}, nullable=False)
    dependents = relationship("Dependent", backref="family")
    visits = relationship("Visit", backref="family")