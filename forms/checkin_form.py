from wtforms import Form, BooleanField, StringField, validators

class CheckinForm(Form):
    stuff = StringField('Stuff', [validators.Length(min=4, max=25)])