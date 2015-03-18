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
    depOrder = 'Dependent.isPrimary.desc()'
    dependents = relationship("Dependent", backref="family", order_by=depOrder)
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
            if not formDependent['isPrimary'].data and \
                (formDependent['firstName'].data == '' and
                 formDependent['lastName'].data == ''):
                continue

            formError = ''

            dependent = Dependent()
            dependent.id = formDependent['id'].data
            dependent.isPrimary = formDependent['isPrimary'].data

            if formDependent['firstName'].data == '':
                formError = 'First name is required'
                formDependent['firstName'].errors.append(formError)
                form.errors['dependent_firstname'] = 'required'
            dependent.firstName = formDependent['firstName'].data

            if formDependent['lastName'].data == '':
                formError = 'Last name is required'
                formDependent['lastName'].errors.append(formError)
                form.errors['dependent_lastname'] = 'required'
            dependent.lastName = formDependent['lastName'].data

            if formDependent['birthdate'].data is None:
                formError = 'Birthday is required'
                formDependent['birthdate'].errors.append(formError)
                form.errors['dependent_birthdate'] = 'required'
            if formDependent['birthdate'].data < datetime(1900, 1, 1):
                formError = 'Birthday must be after 1900'
                formDependent['birthdate'].errors.append(formError)
                form.errors['dependent_birthdate'] = 'required'
                formDependent['birthdate'].data = None
            dependent.birthdate = formDependent['birthdate'].data

            if formError != '':
                raise Exception('Dependent data needed')

            self.dependents.append(dependent)
