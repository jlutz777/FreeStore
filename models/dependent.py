"""
This is the sqlalchemy class for communicating with the dependents table

"""

from sqlalchemy import Column, Integer, Unicode, DateTime, Boolean, ForeignKey
from wtforms import widgets

import models.base as base


class Dependent(base.Base):
    """Sqlalchemy deals model"""
    __tablename__ = "dependents"

    defVal = ''
    idInfo = {}
    idInfo['widget'] = widgets.HiddenInput()
    birthDateInfo = {}
    birthDateInfo["format"] = '%m/%d/%Y'

    id = Column(Integer, primary_key=True, info=idInfo)
    isPrimary = Column('primary', Boolean)
    firstName = Column('first_name', Unicode, nullable=False, default=defVal)
    lastName = Column('last_name', Unicode, nullable=False, default=defVal)
    birthdate = Column('birthdate', DateTime, nullable=True, info=birthDateInfo)
    family_id = Column('family', Integer, ForeignKey('customerfamily.id'))
    relationship = Column('relationship', Integer, ForeignKey('relationships.id'), nullable=True)

    def getDict(self):
        return {
            'id': self.id,
            'fullName': self.firstName + ' ' + self.lastName,
            'family_id': self.family_id
        }
