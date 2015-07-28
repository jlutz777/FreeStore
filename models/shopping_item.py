"""
This is the sqlalchemy class for communicating with the shopping item table

"""

from sqlalchemy import Column, Integer, ForeignKey
import models.base as base


class ShoppingItem(base.Base):
    """Sqlalchemy deals model"""
    __tablename__ = "shopping_item"

    catId = 'shopping_category.id'
    visitId = 'visits.id'
    depId = 'dependents.id'

    id = Column(Integer, primary_key=True)
    quantity = Column('quantity', Integer)
    category_id = Column('category', Integer, ForeignKey(catId))
    visit_id = Column('visit', Integer, ForeignKey(visitId))
    dependent_id = Column('dependent', Integer, ForeignKey(depId))
