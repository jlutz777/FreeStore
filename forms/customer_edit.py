from wtforms import Form, validators, DateField, BooleanField, StringField, HiddenField

class DisabledStringField(StringField):
    def __call__(self, **kwargs):
        kwargs['disabled'] = 'disabled'
        return super(DisabledStringField, self).__call__(**kwargs)
        
class CustomerEditForm(Form):
    shopperID = HiddenField('Shopper ID')
    creationDate = DisabledStringField('Created Date')
    email = StringField('Email', [validators.Optional(),validators.Email()])
    phone = StringField('Phone')
    address = StringField('Address')
    city = StringField('City')
    state = StringField('State')
    zip = StringField('Zip')