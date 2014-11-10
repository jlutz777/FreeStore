from wtforms import Form, validators, DateField, BooleanField, StringField, FieldList, FormField

class DependentForm(Form):
    name = StringField('Name')
    birthday = DateField('Birthday', format='%m/%d/%Y')
    #birthday = StringField('Birthday')
    
class CheckinForm(Form):
    shopperName = StringField('Shopper Name', [validators.Required()])
    shopperBirthday = DateField('Shopper Birthday', [validators.Required()], format='%m/%d/%Y')
    email = StringField('Email', [validators.Optional(),validators.Email()])
    phone = StringField('Phone')
    address = StringField('Address')
    city = StringField('City')
    state = StringField('State')
    zip = StringField('Zip')
    dependents = FieldList(FormField(DependentForm))
    #dependentName = StringField('Dependent Name')
    #dependentBirthday = DateField('Dependent Birthday', [validators.Optional()], format='%m/%d/%Y')