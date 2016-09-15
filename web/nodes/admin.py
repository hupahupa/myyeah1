from flask import Blueprint, render_template, request, url_for, redirect, current_app, session
from flask_login import login_user, logout_user, current_user, login_required
from web.cache import cache
from web.utils import seo, helper
from web.models.user import User
from web.models.user import Video
from web.models.common import db
from web.forms.login_form import LoginFormAdmin
from flask.ext.principal import Identity, identity_changed, AnonymousIdentity
from web.utils.report import *

admin = Blueprint('admin  ', __name__)

@admin.route('/admin/home')
def admin_home():
    return render_template('admin/home.html')

@admin.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = LoginFormAdmin()
    if request.method == 'POST' and form.validate_on_submit():
        user = form.user
        login_user(user)
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
        return redirect("admin/home")
    return render_template('admin/login.html', form=form)

@admin.route('/admin/users')
def users():
    users = User.findAllByAttributes(
            status=User.STATUS_ACTIVE,
            role="user"
        )
    return render_template('admin/users.html', users=users)


@admin.route('/admin/users/<user_id>/videos')
def videos(user_id):
    user = User.findById(user_id)
    return render_template('admin/videos.html', user=user)


@admin.route('/admin/video_report/<video_id>')
def admin_video_report(video_id):
    v = Video.findById(video_id)
    user_id = v.user_id
    if not v.fb_video_id or not v.yt_video_id:
        return redirect("admin/users/%s/videos" % (user_id))

    return render_template('admin/video_report.html',
        facebook_data=gather_facebook_report(v),
        youtube_data=gather_youtube_report(v),
        dailymotion_data=gather_dailymotion_report(v),
        user_id=user_id)

@admin.route('/admin/logout')
def admin_logout():
    logout_user()
    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                            identity=AnonymousIdentity())
    #return redirect(url_for('user_route.signin'))
    return redirect('/')
