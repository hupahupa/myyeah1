from flask import Blueprint, render_template, url_for, redirect, current_app as app
from web.cache import cache
from web.utils import seo
import requests
import json

home = Blueprint('home  ', __name__)

@home.route('/')
def index():
    # update meta data for index
    seo.updateMetaData(
        title="uPaty - the best way to plan you party!",
        wtti="uPaty - the best way to plan you party!",
        keywords="uPaty",
        description="uPaty help you plan your party in the simplest way. Let's party with your friend now!",
        images="uPaty",
    )
    return render_template('home/index.html')