"""
This is the sqlalchemy class for communicating with the shopping item table

"""

from sqlalchemy import Column, Integer, Unicode, ForeignKey
import base

class ShoppingItem(base.Base):
    """Sqlalchemy deals model"""
    __tablename__ = "shopping_item"

    id = Column(Integer, primary_key=True)
    name = Column('name', Unicode)
    category_id = Column('category', Integer, ForeignKey('shopping_category.id'))
    visit_id = Column('visit', Integer, ForeignKey('visits.id'))
