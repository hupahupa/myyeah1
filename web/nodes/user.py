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
from web.utils.report import *
import subprocess
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
    path=os.path.abspath(os.path.join(current_app.config['UPLOAD_FOLDER'], v.filename))

    active_env = ". /home/web/.virtualenvs/web/bin/activate"
    change_folder = "cd %s" % (current_app.config['CONFIG_FOLDER'])
    upload_cmd = "python yt_upload.py --file='%s' --title='%s' --description='This is video upload from Yeah1 app' --keywords='yeah1,video' --category='22' --privacyStatus='public'" % (path, v.name)

    print active_env
    print change_folder
    print upload_cmd

    output = subprocess.check_output('%s && %s && %s' % (active_env, change_folder, upload_cmd),
     shell=True,stderr=subprocess.STDOUT)

    pos = output.find("Video id")
    p = pos+10 # Shift 10 chars, for string Video id '
    youtube_id = output[p:p+11]

    v_url = "https://www.youtube.com/watch?v=%s" % (youtube_id)
    v.yt_url = v_url
    v.yt_video_id = youtube_id

    db.session.add(v)
    db.session.commit()
    return redirect("user/videos")

@user.route('/user/connect_dm')
def connect_dm():
    return render_template('user/home.html')

@user.route('/user/videos')
def user_videos():
    return render_template('user/videos.html', user=current_user)

@user.route('/user/video_report/<video_id>')
def video_report(video_id):
    v = Video.findById(video_id)
    if not v.fb_video_id or not v.yt_video_id:
        return redirect("user/videos")

    return render_template('user/video_report.html',
        facebook_data=gather_facebook_report(v),
        youtube_data=gather_youtube_report(v),
        dailymotion_data=gather_dailymotion_report(v))

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