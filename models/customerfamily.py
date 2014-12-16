"""
This is the sqlalchemy class for communicating with the database.

"""

from datetime import datetime

from sqlalchemy import Column, Integer, Unicode, DateTime
from sqlalchemy.orm import relationship
import base

from models.dependent import Dependent


class CustomerFamily(base.Base):
    """Sqlalchemy deals model"""
    __tablename__ = "customerfamily"

    id = Column(Integer, primary_key=True)
    email = Column('email', Unicode, default=unicode(''))
    phone = Column('phone', Unicode, default=unicode(''))
    address = Column('address', Unicode, default=unicode(''))
    city = Column('city', Unicode, default=unicode(''), nullable=False)
    state = Column('state', Unicode, default=unicode(''), nullable=False)
    zip = Column('zip', Unicode, default=unicode(''), nullable=False)
    datecreated = Column('datecreated', DateTime, nullable=False)
    dependents = relationship("Dependent", backref="family")
    visits = relationship("Visit", backref="family")

    def fromForm(self, id, form):
        if id is not None:
            self.id = id
            self.datecreated = form.datecreated.data
        else:
            self.datecreated = datetime.now()

        self.email = form.email.data
        self.phone = form.phone.data
        self.address = form.address.data
        self.city = form.city.data
        self.state = form.state.data
        self.zip = form.zip.data

        for formDependent in form.dependents:
            dependent = Dependent()
            dependent.id = formDependent['id'].data
            dependent.isPrimary = formDependent['isPrimary'].data
            dependent.firstName = formDependent['firstName'].data
            dependent.lastName = formDependent['lastName'].data
            dependent.birthdate = formDependent['birthdate'].data
            self.dependents.append(dependent)
