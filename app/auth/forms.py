from wtforms import StringField, PasswordField, BooleanField, \
	SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from app.models import User


class LoginForm(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()])
	password = PasswordField(_l('Password'), validators=[DataRequired()])
	remember_me = BooleanField(_l('Remember Me'))
	submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()])
	email = StringField(_l('Email'), validators=[DataRequired(), Email()])
	password = PasswordField(_l('Password'), validators=[DataRequired()])
	password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField(_l('Register'))

	# Create custom validators. 
	# Pattern validate_<field_name>, WTForms takes those pattern as custom validators 
	# and invokes them in addition to the stock validators.
	# Ensure username is available.
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a differnet username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
	email = StringField(_l('Email'), validators=[DataRequired(), Email()])
	submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
	password = PasswordField(_l('Password'), validators=[DataRequired()])
	password2 = PasswordField(
		_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField(_l('Save new Password'))