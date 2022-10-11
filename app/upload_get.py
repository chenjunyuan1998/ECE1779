from flask import render_template, url_for, request, flash, redirect
from app import webapp, memcache
from flask import json
import os


@webapp.route('/upload_get')
def upload_get():
    return render_template("upload_get.html")

@webapp.route('/get', methods=['POST'])
def get():
    key = request.form.get('key')
    result = memcache.get(key)


    if result == -1:
        response = webapp.response_class(
            response=json.dumps("Unknown key"),
            status=400,
            mimetype='application/json'
        )
        return response
    else:
        print(result)
        return render_template("display_image.html", result=result[4:])


@webapp.route('/upload', methods=['POST'])
def upload():

    key = request.form.get('key')

    new_image = request.files['file']
    fname = os.path.join('app/static/images', key)
    new_image.save(fname)

    #value = request.form.get('file')
    memcache.put(key, fname)
    print(fname)

    response = webapp.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )
    return response

