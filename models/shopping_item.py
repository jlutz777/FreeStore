"""
This is the sqlalchemy class for communicating with the shopping item table

"""

from sqlalchemy import Column, Integer, Unicode, ForeignKey
import base


class ShoppingItem(base.Base):
    """Sqlalchemy deals model"""
    __tablename__ = "shopping_item"

    catId = 'shopping_category.id'
    visitId = 'visits.id'

    id = Column(Integer, primary_key=True)
    name = Column('name', Unicode)
    quantity = Column('quantity', Integer)
    category_id = Column('category', Integer, ForeignKey(catId))
    visit_id = Column('visit', Integer, ForeignKey(visitId))
