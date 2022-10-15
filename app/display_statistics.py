import threading
import time
from multiprocessing import Process

from flask import render_template, url_for, request

import BackendApp.db
from app import webapp, memcache
from flask import json


@webapp.route('/display_statistics')
def display_statistics():
    memcache.updateStats()
    result = BackendApp.db.get_stats()
    return render_template("display_statistics.html", result=result)

