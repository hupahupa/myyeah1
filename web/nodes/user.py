from flask import Blueprint, render_template, request, url_for, redirect, current_app, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from web.cache import cache
from web.utils import seo, helper
from web.models.user import User
from web.models.video import Video
from web.models.common import db
from web.forms.upload_video import UploadVideoForm
from web.forms.login_form import LoginFormUser
from flask.ext.principal import Identity, identity_changed, AnonymousIdentity
from werkzeug.utils import secure_filename
from web.utils import youtube_upload
from collections import namedtuple
from oauth2client.tools import argparser
import requests
import json
import os

user = Blueprint('user  ', __name__)

@user.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginFormUser()
    if request.method == 'POST' and form.validate_on_submit():
        user = form.user
        login_user(user)
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

        return redirect("/user/home")

    return render_template('user/login.html', form=form)

# TODO: just for test
@user.route('/user/createUser')
def createUser():
    d = {"email": "duytestyeah1partner@gmail.com", "password": "duy123456", "role": "user"}
    u, _ = User.create(d)
    db.session.commit()
    return "SUCESS"

@user.route('/user/createAdmin')
def createAdmin():
    d = {"email": "duytestyeah1manage@gmail.com", "password": "duy123456", "role": "admin"}
    u, _ = User.create(d)
    db.session.commit()
    return "SUCESS"

@user.route('/user/home')
def home():
    return render_template('user/home.html')

@user.route('/user/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadVideoForm()
    if request.method == 'POST' and form.validate_on_submit():
        # check if the post request has the file part
        if 'file' not in request.files:
            print 'No file part'
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print 'No selected file'
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1]

            # create video instance
            d = {"name": form.name.data, "user_id": current_user.id}
            v = Video.create(d)
            db.session.commit()

            filename = "%s.%s" % (v.id, ext)
            v.filename = filename
            db.session.add(v)
            db.session.commit()

            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect('/user/videos')
    return render_template('user/upload.html', form=form)

@user.route('/user/upload_facebook/<video_id>')
def upload_facebook(video_id):
    access = current_app.config["FB_ACCESS_TOKEN"]
    fb_page_id = current_app.config["FB_PAGE_ID"]
    v = Video.findById(video_id)

    url='https://graph-video.facebook.com/'+str(fb_page_id)+'/videos?access_token='+str(access)
    path=os.path.join(current_app.config['UPLOAD_FOLDER'], v.filename)

    print "AAAA"
    print path
    print url

    files={'file':open(path,'rb')}
    flag=requests.post(url, files=files).text
    response = json.loads(flag)

    print response

    fb_user_id = current_app.config["FB_PAGE_ID"]
    v_url = 'https://www.facebook.com/'+ str(fb_user_id) +'/videos/'+ str(response["id"])
    v.fb_url = v_url
    v.fb_video_id = response["id"]

    db.session.add(v)
    db.session.commit()
    return redirect("user/videos")

@user.route('/user/upload_youtube/<video_id>')
def upload_youtube(video_id):
    v = Video.findById(video_id)
    path=os.path.join(current_app.config['UPLOAD_FOLDER'], v.filename)
    args = {
        "file": path,
        "title": v.name,
        "description": "This is test description",
        "categoryId": 22,
        "privacyStatus": "public"
    }
    # argparser.add_argument("file", required=True, default=path)
    # argparser.add_argument("title", default=v.name)
    # argparser.add_argument("description", default="Test Description")
    # argparser.add_argument("category", default="22")
    # argparser.add_argument("keywords", default="")
    # argparser.add_argument("privacyStatus", choices="public")
    # args = argparser.parse_args()
    # youtube_upload.do_upload(args)
    return render_template('user/home.html')

@user.route('/user/connect_dm')
def connect_dm():
    return render_template('user/home.html')

@user.route('/user/videos')
def user_videos():
    return render_template('user/videos.html', user=current_user)

@user.route('/user/video_report/<video_id>')
def video_report(video_id):
    access = current_app.config["FB_ACCESS_TOKEN"]
    v = Video.findById(video_id)

    url='https://graph.facebook.com/'+str(v.fb_video_id)+'/video_insights?access_token='+str(access)
    print url
    resp = requests.get(url).text
    resp = json.loads(resp)

    facebook_data=format_facebook_data(resp)
    print facebook_data
    youtube_data={}
    dailymotion_data={}
    return render_template('user/video_report.html',
        facebook_data=facebook_data,
        youtube_data=youtube_data,
        dailymotion_data=dailymotion_data)
def format_facebook_data(resp):
    # access value for single
    single = [
        "total_video_views",
        "total_video_views_unique",
        "total_video_views_autoplayed",
        "total_video_views_clicked_to_play",
        "total_video_views_organic",
        "total_video_views_organic_unique",
        "total_video_views_paid",
        "total_video_views_paid_unique",
        "total_video_views_sound_on",
        "total_video_complete_views",
        "total_video_complete_views_unique",
        "total_video_complete_views_auto_played",
        "total_video_complete_views_clicked_to_play",
        "total_video_complete_views_organic",
        "total_video_complete_views_organic_unique",
        "total_video_complete_views_paid",
        "total_video_complete_views_paid_unique",
        "total_video_10s_views",
        "total_video_10s_views_unique",
        "total_video_10s_views_auto_played",
        "total_video_10s_views_clicked_to_play",
        "total_video_10s_views_organic",
        "total_video_10s_views_paid",
        "total_video_10s_views_sound_on",
        "total_video_avg_time_watched",
        "total_video_view_total_time",
        "total_video_view_total_time_organic",
        "total_video_view_total_time_paid",
        "total_video_impressions",
        "total_video_impressions_unique",
        "total_video_impressions_paid_unique",
        "total_video_impressions_paid",
        "total_video_impressions_organic_unique",
        "total_video_impressions_organic",
        "total_video_impressions_viral_unique",
        "total_video_impressions_viral",
        "total_video_impressions_fan_unique",
        "total_video_impressions_fan",
        "total_video_impressions_fan_paid_unique",
        "total_video_impressions_fan_paid"
    ]
    d = []
    for s in resp.get("data"):
        values = s.get("values")
        val = values[0]
        k = s.get("name")
        if (k in single):
            v = val.get("value")
            d.append((k, v))
        else:
            pass
    return d
@user.route('/user/logout')
def logout():
    logout_user()
    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                            identity=AnonymousIdentity())
    #return redirect(url_for('user_route.signin'))
    return redirect('/')


def allowed_file(filename):
    ALLOWED_EXTENSIONS = current_app.config["ALLOWED_EXTENSIONS"]
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
