"""
This is the sqlalchemy class for communicating with the shopping category table

"""

from sqlalchemy import Column, Integer, Unicode, Boolean
from sqlalchemy.orm import relationship
import models.base as base


class ShoppingCategory(base.Base):
    """Sqlalchemy deals model"""
    __tablename__ = "shopping_category"

    id = Column(Integer, primary_key=True)
    name = Column('name', Unicode)
    dailyLimit = Column('daily_limit', Integer)
    monthlyLimit = Column('monthly_limit', Integer)
    yearlyLimit = Column('yearly_limit', Integer)
    familyWideLimit = Column('family_wide', Boolean)
    order = Column('order', Integer)
    minAge = Column('min_age', Integer, nullable=True)
    maxAge = Column('max_age', Integer, nullable=True)
    disabled = Column('disabled', Boolean)
    items = relationship("ShoppingItem", backref="category")

    def fromForm(self, posted):
        self.name = posted.name
        self.dailyLimit = posted.dailyLimit
        self.monthlyLimit = posted.monthlyLimit
        self.yearlyLimit = posted.yearlyLimit
        self.familyWideLimit = posted.familyWideLimit != ""
        self.order = posted.order
        minAge = posted.minAge
        if minAge == "":
            minAge = 0
        self.minAge = minAge
        maxAge = posted.maxAge
        if maxAge == "":
            maxAge = 150
        self.maxAge = maxAge
        self.disabled = posted.catDisabled != ""

    def getDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'dailyLimit': self.dailyLimit,
            'monthlyLimit': self.monthlyLimit,
            'yearlyLimit' : self.yearlyLimit,
            'familyWideLimit': self.familyWideLimit,
            'order': self.order,
            'minAge': self.minAge,
            'maxAge': self.maxAge,
            'disabled': self.disabled
        }
