from collections import OrderedDict
from datetime import datetime

from wtforms import Form, validators, DateField, BooleanField, StringField, HiddenField, FormField
from wtforms_alchemy import ModelForm, ModelFieldList

from models import CustomerFamily, Dependent

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
            },
            'birthdate': {
                'validators' : [validators.InputRequired()]
            }
        }

class CustomerForm(ModelForm):
    class Meta:
        datetime_format = '%m/%d/%Y'
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
            'datecreated': {
                'validators' : [validators.Optional()]
            }
        }

    dependents = ModelFieldList(FormField(DependentForm), min_entries=1)