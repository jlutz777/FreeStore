"""
This is the sqlalchemy class for communicating with the shopping category table

"""

from sqlalchemy import Column, Integer, Unicode
import base

class ShoppingCategory(base.Base):
    """Sqlalchemy deals model"""
    __tablename__ = "shopping_category"

    id = Column(Integer, primary_key=True)
    name = Column('name', Unicode)
    dailyLimit = Column('daily_limit', Integer)
