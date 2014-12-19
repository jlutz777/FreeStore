"""
This is the sqlalchemy class for communicating with the visits table

"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

import base

from models.shopping_item import ShoppingItem
from models.customerfamily import CustomerFamily


class Visit(base.Base):
    """Sqlalchemy deals model"""
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True)
    checkin = Column('checkin', DateTime)
    checkout = Column('checkout', DateTime)
    family_id = Column('family', Integer, ForeignKey('customerfamily.id'))
    items = relationship("ShoppingItem", backref="visit")

    def setStatus(self, status, family_id, id=None):
        self.family_id = family_id
        if (status == 'checkin'):
            self.checkin = datetime.now()

    def fromForm(self, id, form, db):
        self.id = id
        self.checkin = form.checkin.data
        self.checkout = datetime.now()

        customerQuery = db.query(CustomerFamily)
        fam = customerQuery.filter(CustomerFamily.id == form.family_id.data)[0]

        self.family = fam

        for formItem in form.items:
            item = ShoppingItem()
            item.id = formItem['id'].data
            item.name = formItem['name'].data
            item.category_id = formItem['category_id'].data
            self.items.append(item)
