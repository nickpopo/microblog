from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from app.models import User



class EditProfileForm(FlaskForm):
	username = StringField(_l(_l('Username')), validators=[DataRequired()])
	about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])
	submit = SubmitField(_l('Submit'))

	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username.')


class PostForm(FlaskForm):
	post = TextAreaField(_l('Say something'), validators=[DataRequired(), Length(min=1, max=140)])
	submit = SubmitField(_l('Submit'))