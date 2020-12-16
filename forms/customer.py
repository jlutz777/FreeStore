from wtforms import validators, FormField, SelectField
from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms.fields import DateTimeField

from models import CustomerFamily, Dependent, Relationship


class RelationshipForm(ModelForm):
    class Meta:
        datetime_format = '%m/%d/%Y'
        model = Relationship
        include = ['id']
        field_args = {
            'id': {
                'validators': [validators.Optional()]
            },
            'name': {
                'validators': [validators.Optional()]
            }
        }


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

    # This should be queried from the db
    relationship = SelectField(u'Relationship', coerce=int, \
                    validators=[validators.Optional()], \
                    choices=[(1, 'Spouse/significant other'),(2, 'Child'),
                             (3, 'Grandparent'), (4, 'Grandchild'),
                             (5, 'Other')])


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
