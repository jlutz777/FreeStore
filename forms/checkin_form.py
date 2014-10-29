from wtforms import Form, validators, DateField, BooleanField, StringField

class CheckinForm(Form):
    shopperName = StringField('Shopper Name', [validators.Required()])
    shopperBirthday = DateField('Shopper Birthday', [validators.Required()])
    
#Name of shopper
#Birthdate of shopper
#Email of shopper
#Phone of shopper
#Address of shopper
#Zip code of shopper
#Dependent* name
#Dependent birthday
#Automatic date and time stamp
#Assign a unique and permanent shopper number
