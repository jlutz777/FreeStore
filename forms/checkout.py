from wtforms import Form, validators, DateField, BooleanField, StringField, HiddenField, FormField
from wtforms_alchemy import ModelForm, ModelFieldList

from models import ShoppingItem, Visit, ShoppingCategory

class CategoryForm(ModelForm):
    class Meta:
        model = ShoppingCategory
        include = ['id']
        field_args = {
            'id': {
                'validators': [validators.InputRequired()]
            },
            'name': {
                'validators': [validators.Optional()]
            },
            'dailyLimit': {
                'validators': [validators.Optional()]
            }
        }

class ShoppingItemForm(ModelForm):
    class Meta:
        datetime_format = '%m/%d/%Y'
        model = ShoppingItem
        field_args = {
            'name': {
                'validators' : [validators.Optional()]
            }
        }

    category = FormField(CatgoryForm)

class CheckoutForm(ModelForm):
    class Meta:
        datetime_format = '%m/%d/%Y'
        model = Visit
        include = ['id']
        field_args = {
            'id' : {
                'validators' : [validators.InputRequired()]
            },
            'checkin': {
                'validators' : [validators.InputRequired()]
            },
            'checkout': {
                'validators' : [validators.Optional()]
            },
            'family_id': {
                'validators' : [validators.InputRequired()]
            }
        }

    items = ModelFieldList(FormField(ShoppingItemForm), min_entries=0)