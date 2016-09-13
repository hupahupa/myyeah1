from flask_wtf import Form
from wtforms import fields
from wtforms import validators
from web.models.user import User

class LoginFormUser(Form):
    email = fields.TextField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate(self):
        Form.validate(self)
        if self.email.errors or self.password.errors:
            return False

        user = User.query.filter(User.email == self.email.data).first()

        if user is None:
            self.email.errors.append('Invalid login')
            return False

        if not user.is_valid_password(self.password.data):
            self.password.errors.append('Invalid login')
            return False

        if user.status != User.STATUS_ACTIVE:
            self.email.errors.append('Your account is not active yet.')
            return False
        self.user = user
        return True

class LoginFormAdmin(Form):
    email = fields.TextField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate(self):
        Form.validate(self)
        if self.email.errors or self.password.errors:
            return False

        user = User.query.filter(User.email == self.email.data).first()

        if user is None:
            self.email.errors.append('Invalid login')
            return False

        if not user.is_valid_password(self.password.data):
            self.password.errors.append('Invalid login')
            return False

        if user.status != User.STATUS_ACTIVE:
            self.email.errors.append('Your account is not active yet.')
            return False
        self.user = user
        return True