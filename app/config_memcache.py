from flask import render_template, url_for, request,flash

import BackendApp.db
from app import webapp, memcache
from flask import json


@webapp.route('/config_Memcache')
def config_memcache():
    return render_template("config_memcache.html")

@webapp.route('/setConfig', methods=['POST'])
def set_configure():

    capacity = request.form.get('capacity')
    policy = request.form.get('policy')
    #check if the capacity is number
    if capacity.isdigit():
        BackendApp.db.put_config(capacity,policy)
        memcache.refreshConfiguration()
        memcache.clear()

        response = webapp.response_class(
        response=json.dumps("Success"),
        status=200,
        mimetype='application/json'
       )
        return response
    else:
        flash("Please enter a number for capacity!")
        return render_template("config_memcache.html")


@webapp.route('/clearCache', methods=['POST'])
def clear_cache():
    memcache.clear()
    response = webapp.response_class(
        response=json.dumps("Success"),
        status=200,
        mimetype='application/json'
    )
    return response

