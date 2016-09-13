from flask_wtf import Form
from wtforms import fields
from wtforms import validators

class UploadVideoForm(Form):
    name = fields.TextField(validators=[validators.InputRequired()])

    def validate(self):
        Form.validate(self)
        if self.name.errors:
            return False
        return True