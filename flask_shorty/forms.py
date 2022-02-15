from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length

# Form Models
class CreateForm(FlaskForm):
    long_url = StringField('Long Url (to be shortened)',
                           validators=[DataRequired(),
                                       Length(min=20, max=200)])
    name = StringField('Name (reference required)', validators=[DataRequired()])
    expiry_time = DateTimeField('(Optional) I would like my link to expire at exactly:', format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField('Generate shorter url')

class FindForm(FlaskForm):
    name = StringField('Name (reference required)', validators=[DataRequired()])
    submit = SubmitField('Retrieve')


class UpdateForm(FlaskForm):
    name = StringField('Name (reference required)', validators=[DataRequired()])
    expiry_time = DateTimeField('(Optional) Update Expiry Time:', format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField('Update')