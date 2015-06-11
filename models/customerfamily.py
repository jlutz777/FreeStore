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
    comments = Column('comments', Unicode, default=unicode(''))
    checkoutComments = Column('checkoutcomments', Unicode, default=unicode(''))
    adminComments = Column('admincomments', Unicode, default=unicode(''))
    depOrder = 'Dependent.isPrimary.desc()'
    dependents = relationship("Dependent", backref="family", order_by=depOrder)
    visits = relationship("Visit", backref="family", lazy="dynamic")

    def __checkFirstName__(self, formDependent, form):
        hasError = False
        if formDependent['firstName'].data == '':
            formError = 'First name is required'
            formDependent['firstName'].errors.append(formError)
            form.errors['dependent_firstname'] = 'required'
            hasError = True
        return hasError

    def __checkLastName__(self, formDependent, form):
        hasError = False
        if formDependent['lastName'].data == '':
            formError = 'Last name is required'
            formDependent['lastName'].errors.append(formError)
            form.errors['dependent_lastname'] = 'required'
            hasError = True
        return hasError

    def __checkBirthDate__(self, formDependent, form):
        hasError = False
        if formDependent['birthdate'].data is None:
            formError = 'Birthday is required'
            formDependent['birthdate'].errors.append(formError)
            form.errors['dependent_birthdate'] = 'required'
            hasError = True
        elif formDependent['birthdate'].data < datetime(1900, 1, 1):
            formError = 'Birthday must be after 1900'
            formDependent['birthdate'].errors.append(formError)
            form.errors['dependent_birthdate'] = 'required'
            formDependent['birthdate'].data = None
            hasError = True
        return hasError

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
        self.comments = form.comments.data
        self.adminComments = form.adminComments.data

        for formDependent in form.dependents:
            if not formDependent['isPrimary'].data and \
                (formDependent['firstName'].data == '' and
                 formDependent['lastName'].data == ''):
                continue

            dependent = Dependent()
            dependent.id = formDependent['id'].data
            dependent.isPrimary = formDependent['isPrimary'].data

            hasError = self.__checkFirstName__(formDependent, form)
            dependent.firstName = formDependent['firstName'].data

            if self.__checkLastName__(formDependent, form):
                hasError = True
            dependent.lastName = formDependent['lastName'].data

            if self.__checkBirthDate__(formDependent, form):
                hasError = True
            dependent.birthdate = formDependent['birthdate'].data

            if hasError:
                raise Exception('Dependent data needed')

            self.dependents.append(dependent)
