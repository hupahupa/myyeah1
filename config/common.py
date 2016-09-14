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
    'FB_PAGE_ID': '266115127115395',
    # Fanpage Access Token
    'FB_ACCESS_TOKEN': 'EAACXZBm8HwvsBAFe9UIr3UJEw1m9m64I7JrTDqv7pAxxsrD7tErjSpqZAg0kbFoUgKo31LadcKSHRn7ZBZBfxXR3XtxKfX65Ms2CnMO3i9dgbfZAMPAlMHEAxQFtUNZBUqUpEXkIAoGb9NddZAlz206Vi4zrs3tMpPg5MojJmYaBNYMxpFecUzQ',
    'LANGUAGES': (
        ('vi', u'Tiếng Việt'),
        ('en', u'English')
    ),
    'english_domains': ['upaty.com', 'dev.upaty.com']
}
