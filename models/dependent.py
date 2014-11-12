"""
This is the sqlalchemy class for communicating with the dependents table

"""

from sqlalchemy import Column, Integer, Unicode, DateTime, Boolean, ForeignKey
from wtforms import widgets
from wtforms.validators import Optional

import base

class Dependent(base.Base):
    """Sqlalchemy deals model"""
    __tablename__ = "dependents"

    id = Column(Integer, primary_key=True, info={'widget': widgets.HiddenInput()})
    isPrimary = Column('primary', Boolean, info={'label': 'Primary'})
    firstName = Column('first_name', Unicode, info={'label': 'First Name'})
    lastName = Column('last_name', Unicode, info={'label': 'Last Name'})
    birthdate = Column('birthdate', DateTime, info={'format': '%m/%d/%Y', 'label': 'Birthday'})
    family_id = Column('family', Integer, ForeignKey('customerfamily.id'))
