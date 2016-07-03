from wtforms import validators, FormField
from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms.fields import DateTimeField

from models import CustomerFamily, Dependent


class DependentForm(ModelForm):
    class Meta:
        datetime_format = '%m/%d/%Y'
        model = Dependent
        include = ['id']
        field_args = {
            'id': {
                'validators': [validators.Optional()]
            },
            'firstName': {
                'validators': [validators.Optional()]
            },
            'lastName': {
                'validators': [validators.Optional()]
            },
            'birthdate': {
                'validators': [validators.Optional()]
            }
        }


class CustomerForm(ModelForm):
    volunteer_date = DateTimeField(format='%m/%d/%Y %H:%M',
                        validators=(validators.Optional(),))
    
    class Meta:
        datetime_format = '%m/%d/%Y'
        model = CustomerFamily
        field_args = {
            'id': {
                'validators': [validators.Optional()]
            },
            'city': {
                'validators': [validators.InputRequired()]
            },
            'state': {
                'validators': [validators.InputRequired()]
            },
            'zip': {
                'validators': [validators.InputRequired()]
            },
            'datecreated': {
                'validators': [validators.Optional()]
            }
        }

    dependents = ModelFieldList(FormField(DependentForm), min_entries=2)
