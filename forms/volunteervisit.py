from wtforms import validators
from wtforms_alchemy import ModelForm

from models import VolunteerVisit


class VisitForm(ModelForm):
    class Meta:
        datetime_format = '%m/%d/%Y %H:%M'
        model = VolunteerVisit
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
