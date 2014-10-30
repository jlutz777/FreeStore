from wtforms import Form, validators, DateField, BooleanField, StringField

class CheckinForm(Form):
    shopperName = StringField('Shopper Name', [validators.Required()])
    shopperBirthday = DateField('Shopper Birthday', [validators.Required()], format='%m/%d/%Y')
    email = StringField('Email', [validators.Optional(),validators.Email()])
    phone = StringField('Phone')
    address = StringField('Address')
    city = StringField('City')
    state = StringField('State')
    zip = StringField('Zip')
    dependentName = StringField('Dependent Name')
    dependentBirthday = DateField('Dependent Birthday', [validators.Optional()], format='%m/%d/%Y')
