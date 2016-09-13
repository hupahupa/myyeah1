import traceback
from flask import Flask, render_template, current_app, redirect, flash
from flask_principal import Principal, identity_loaded, RoleNeed, UserNeed
from flask_login import current_user
from flask_babelex import Babel, lazy_gettext
from web.models.common import db
from config.main import config
from web.nodes.home import home
from web.nodes.user import user
from web.nodes.admin import admin
from web.utils.flask_ajaxform import FlaskAjaxForm
from web.cache import cache
from web.utils import seo
from web.utils.auth import login_manager

app = Flask(__name__)
app.config.update(config)
app.debug = config.get("debug", False)

db.init_app(app)
login_manager.init_app(app)

# Web blueprints
app.register_blueprint(home)
app.register_blueprint(admin)
app.register_blueprint(user)

form = FlaskAjaxForm(app)
principals = Principal(app)
babel = Babel(app)
cache.init_app(app)

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if current_user:
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if current_user.id and current_user.role:
        identity.provides.add(RoleNeed(current_user.role))


from web.utils import helper
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.jinja_env.globals.update({
    'enumerate': enumerate,
    'str':str,
    'len':len,
    'getattr': getattr,
    'format_datetime': helper.format_datetime,
    'format_date': helper.format_date,
    'format_time': helper.format_time,
    'current_app': current_app,
    'getLocale': helper.getLocale,
    'seo': seo,
    'helper': helper
})

@babel.localeselector
def get_locale():
    return helper.getLocale()


@app.errorhandler(403)
@cache.cached(timeout=60*60*24)
def permission_denied(e):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
@cache.cached(timeout=60*60*24)
def page_not_found(e):
    return render_template('errors/404.html'), 404
