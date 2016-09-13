# -*- coding: utf-8 -*-
import pytz
import bcrypt
from datetime import datetime
from common import db, UTCDateTime, Base
from web.models.video import Video
from flask_login import UserMixin
from flask import current_app as app, url_for
from web.utils import helper
from sqlalchemy import or_

class User(UserMixin, Base, db.Model):
    __tablename__ = "tbl_user"

    ##############
    # Attributes #
    ##############
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.UnicodeText())
    fb_id = db.Column(db.UnicodeText(), unique=True)
    email = db.Column(db.UnicodeText(), unique=True)
    password = db.Column(db.UnicodeText())
    secret_token = db.Column(db.UnicodeText(), unique=True)
    role = db.Column(db.UnicodeText())

    STATUS_PEDING = u"pending"
    STATUS_ACTIVE = u"active"
    status = db.Column(db.Enum([
        STATUS_PEDING, STATUS_ACTIVE
    ], native_enum=False), nullable=False, default=STATUS_PEDING)
    created_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))
    avatar = db.Column(db.UnicodeText())
    fb_token = db.Column(db.UnicodeText())

    videos = db.relationship('Video', backref='user', lazy='dynamic', foreign_keys='Video.user_id', order_by='Video.id')

    ####################
    # Instance methods #
    ####################
    def __repr__(self):
        return '<User id: %s, full_name: %s>' % (self.id, self.full_name)

    # Contruction
    def __init__(self, email, password):
        self.email = email

        # TODO: Update this when user register by email, password
        if password:
            self.password = self._hash_password(password)
        else:
            self.password = self._hash_password(helper.generate_string())

        self.secret_token = helper.generate_string()

        # TODO: Also update this later
        self.status = self.STATUS_ACTIVE

    # Hash the pasword
    def _hash_password(self, password):
        return bcrypt.hashpw(
            password,
            bcrypt.gensalt())

    def is_valid_password(self, password):
         hashed = self.password.encode("utf-8")
         return bcrypt.hashpw(password, hashed) == hashed

    # Create user with data
    @classmethod
    def create(cls, data):
        email = data.get('email', None)
        password = data.get('password', None)
        role = data.get('role', 'user')
        # user = cls.query.filter(cls.email == email).first()

        # if user:
        #     # user instance and is_new
        #     return user, False

        user = cls(email, password)
        user.role = role
        db.session.add(user)
        # user instance and is_new
        return user, True