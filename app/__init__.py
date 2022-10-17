from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask


import BackendApp.MemCache

#global memcache

webapp = Flask(__name__)
webapp.secret_key = 'secret key'
memcache = BackendApp.MemCache.MemCache(12,"LRU")
db = BackendApp.db

#the scheduler make memcache to store status to db every 5 second
scheduler = BackgroundScheduler({'apscheduler.timezone': 'EST'})
scheduler.add_job(func=memcache.updateStats, trigger="interval", seconds=5)
scheduler.start()

from app import main
from app import upload_get
from app import display_statistics
from app import display_key
from app import display_image
from app import config_memcache
from app import api











