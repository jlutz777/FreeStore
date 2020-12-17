"""
This is the sqlalchemy class for communicating with the relationships table

"""

from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import relationship
from wtforms import widgets

import models.base as base


class Relationship(base.Base):
    """Sqlalchemy deals model"""
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True)
    name = Column('name', Unicode, nullable=False)

    def getDict(self):
        return {
            'id': self.id,
            'name': self.name
        }
