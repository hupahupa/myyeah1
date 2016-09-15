# -*- coding: utf-8 -*-
import pytz
import bcrypt
from datetime import datetime
from common import db, UTCDateTime, Base
from flask import current_app as app, url_for

class Video(Base, db.Model):
    __tablename__ = "tbl_video"

    ##############
    # Attributes #
    ##############
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText())
    user_id = db.Column(db.Integer, db.ForeignKey('tbl_user.id'))
    description = db.Column(db.UnicodeText())
    filename = db.Column(db.UnicodeText())
    fb_url = db.Column(db.UnicodeText())
    fb_video_id = db.Column(db.UnicodeText())
    yt_video_id = db.Column(db.UnicodeText())
    yt_url = db.Column(db.UnicodeText())
    dm_url = db.Column(db.UnicodeText())
    created_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))
    updated_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))

    ####################
    # Instance methods #
    ####################
    def __repr__(self):
        return '<Video id: %s, name: %s>' % (self.id, self.name)

    # Contruction
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    # Create user with data
    @classmethod
    def create(cls, data):
        name = data.get('name', None)
        user_id = data.get('user_id', None)
        v = cls(name, user_id)
        db.session.add(v)
        return v