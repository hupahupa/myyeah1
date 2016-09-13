from flask_login import AnonymousUserMixin, LoginManager

from web.models.user import User

login_manager = LoginManager()

class AnonymousUser(AnonymousUserMixin):
    id = None


login_manager.anonymous_user = AnonymousUser
login_manager.login_view = "user.login"


@login_manager.user_loader
def load_user(user_id):
    return User.findById(user_id)
