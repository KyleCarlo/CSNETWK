from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class Console(FlaskForm):
    console_input_field = StringField('Console', validators=[DataRequired()], id='console')
    console_submit = SubmitField('Enter', id='console')

class Message(FlaskForm):
    message_input_field = StringField('Message', validators=[DataRequired()], id='message')
    message_submit = SubmitField('Send', id='message')