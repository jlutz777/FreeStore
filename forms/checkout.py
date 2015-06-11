from wtforms import validators, FormField, SelectField
from wtforms_alchemy import ModelForm, ModelFieldList

from models import ShoppingItem, Visit, ShoppingCategory


class CategoryForm(ModelForm):
    class Meta:
        model = ShoppingCategory
        include = ['id']
        '''field_args = {
            'id': {
                'validators': [validators.InputRequired()]
            },
            'name': {
                'validators': [validators.Optional()]
            },
            'dailyLimit': {
                'validators': [validators.Optional()]
            }
        }'''


class ShoppingItemForm(ModelForm):
    class Meta:
        model = ShoppingItem
        include = ['id']
        field_args = {
            'id': {
                'validators': [validators.Optional()]
            },
            'name': {
                'validators': [validators.Optional()]
            }
        }

    category = SelectField(u'Category', coerce=int)


class CheckoutForm(ModelForm):
    class Meta:
        datetime_format = '%m/%d/%Y %H:%M:%S'
        model = Visit
        include = ['id', 'family_id']
        field_args = {
            'id': {
                'validators': [validators.Optional()]
            },
            'checkin': {
                'validators': [validators.InputRequired()]
            },
            'checkout': {
                'validators': [validators.Optional()]
            },
            'family_id': {
                'validators': [validators.InputRequired()]
            }
        }

    items = ModelFieldList(FormField(ShoppingItemForm), min_entries=0)
