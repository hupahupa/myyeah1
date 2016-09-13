# -*- coding: utf-8 -*-
import os
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = CONFIG_DIR.rsplit('/', 1)[0]

ALLOWED_EXTENSIONS = set(['avi', 'mp4'])
UPLOAD_FOLDER = "web/static/uploads"
config = {
    'DOMAIN': 'upaty.com',
    'MAX_CONTENT_LENGTH': 2 * 1024 * 1024,
    'DATETIME_FORMAT': "%d-%m-%Y %H:%M",
    'DATE_FORMAT': '%d-%m-%Y',
    'TIME_FORMAT': '%H:%M',
    'SECRET_KEY': 'flask-session-insecure-secret-key',
    'SQLALCHEMY_DATABASE_URI': '',
    'SQLALCHEMY_ECHO': False,
    'CSS_SYNC_PORT': 9264,
    'debug': True,
    'email': {
    },
    'ALLOWED_EXTENSIONS': ALLOWED_EXTENSIONS,
    'UPLOAD_FOLDER': UPLOAD_FOLDER,
    'FB_APP_ID': '167101860397819',
    'FB_APP_SECRET': 'dd6cbcd78edea6bc66aec061609a8d7a',
    'FB_ID': '132800883842221',
    'FB_USER_ID': '100013369306991',
    'FB_ACCESS_TOKEN': 'EAACXZBm8HwvsBADKJFJZB9ZBTviPDpMm6kBhoNfGhxEo0EsgQcbrHDRsacdv2IZBAoUzvOsL882EV9ZAgSsChArBCKoizUIusjpvodwpRZC8F19gL54ooeTq1XKWJYltXyE6IovvfO82e69LqNJZAhjZBi6d1q8Dvcl4zCmWDDbBpwZDZD',
    'LANGUAGES': (
        ('vi', u'Tiếng Việt'),
        ('en', u'English')
    ),
    'english_domains': ['upaty.com', 'dev.upaty.com']
}
