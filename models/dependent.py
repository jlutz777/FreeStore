"""
This is the sqlalchemy class for communicating with the dependents table

"""

from sqlalchemy import Column, Integer, Unicode, DateTime, Boolean, ForeignKey
import base

class Dependent(base.Base):
    """Sqlalchemy deals model"""
    __tablename__ = "dependents"

    id = Column(Integer, primary_key=True)
    isPrimary = Column('primary', Boolean)
    firstName = Column('first_name', Unicode)
    lastName = Column('last_name', Unicode)
    birthdate = Column('birthdate', DateTime)
    family_id = Column('family', Integer, ForeignKey('customerfamily.id'))
