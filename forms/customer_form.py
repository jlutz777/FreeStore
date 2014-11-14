from collections import OrderedDict

from wtforms import Form, validators, DateField, BooleanField, StringField, HiddenField, FormField
from wtforms_alchemy import ModelForm, ModelFieldList

from models import CustomerFamily, Dependent

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

class DependentForm(ModelForm):
    class Meta:
        datetime_format = '%m/%d/%Y'
        model = Dependent
        include = ['id']
        field_args = {
            'id' : {
                'validators' : [validators.Optional()]
            },
            'firstName': {
                'validators' : [validators.InputRequired()]
            },
            'lastName': {
                'validators' : [validators.InputRequired()]
            }
        }

class CustomerForm(ModelForm):
    class Meta:
        model = CustomerFamily
        field_args = {
            'id' : {
                'validators' : [validators.Optional()]
            },
            'city': {
                'validators' : [validators.InputRequired()]
            },
            'state': {
                'validators' : [validators.InputRequired()]
            },
            'zip': {
                'validators' : [validators.InputRequired()]
            },
            'state': {
                'validators' : [validators.InputRequired()]
            }
        }
        
    datecreated = DisabledStringField('Created Date')
    dependents = ModelFieldList(FormField(DependentForm), min_entries=1)

    '''def __iter__(self):
        # Total hack to get dependents at the end of the list
        last_field = self._fields.popitem(False)
        temp_fields = OrderedDict()
        for name, val in self._fields.items():
            temp_fields[name] = val
        temp_fields[last_field[0]] = last_field[1]
        self._fields = temp_fields
        
        return super(CustomerForm, self).__iter__()
    '''