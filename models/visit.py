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

    def fromPost(self, visit_id, posted, categories, db):
        self.id = visit_id
        self.checkin = posted["checkin"]
        self.checkout = datetime.now()

        customerQuery = db.query(CustomerFamily)
        fam = customerQuery.filter(CustomerFamily.id == posted["family_id"])[0]

        self.family = fam

        for dependent in fam.dependents:
            for category in categories:
                itemKey = "row_" + str(dependent.id)
                itemKey += "_col_" + str(category[0])
                thisShoppingItem = posted.get(itemKey, "")
                if thisShoppingItem != "" and thisShoppingItem != "0":
                    item = ShoppingItem()
                    # for editing:  item.id = ???
                    item.category_id = category[0]
                    item.dependent_id = dependent.id
                    item.quantity = thisShoppingItem
                    self.items.append(item)
