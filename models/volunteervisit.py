"""
This is the sqlalchemy class for communicating with the visits table

"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey

import models.base as base


class VolunteerVisit(base.Base):
    """Sqlalchemy deals model"""
    __tablename__ = "volunteervisits"

    id = Column(Integer, primary_key=True)
    checkin = Column('checkin', DateTime)
    checkout = Column('checkout', DateTime)
    family_id = Column('family', Integer, ForeignKey('customerfamily.id'))

    def fromForm(self, form):
        # Ensure if there is no id data, it gets marked as None so
        # the db creates a new volunteer visit
        if form.id.data is not None and form.id.data != '':
            self.id = form.id.data
        else:
            self.id = None
        self.checkin = form.checkin.data
        self.checkout = form.checkout.data
        self.family_id = form.family_id.data
