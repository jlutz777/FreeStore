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
    email = Column('email', Unicode)
    phone = Column('phone', Unicode, default=unicode(''))
    address = Column('address', Unicode)
    city = Column('city', Unicode)
    state = Column('state', Unicode)
    zip = Column('zip', Unicode)
    datecreated = Column('datecreated', DateTime)
    dependents = relationship("Dependent", backref="family")
    visits = relationship("Visit", backref="family")