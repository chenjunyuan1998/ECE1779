import base64
import sys
from base64 import b64encode

from flask import render_template, url_for, request, flash, redirect

import BackendApp.db
from app import webapp, memcache
from flask import json
import os


@webapp.route('/upload_search')
def upload_search():
    return render_template("upload_search.html")

@webapp.route('/search', methods=['POST'])
def search():

    key = request.form.get('key')
    result = memcache.get(key)

    response = webapp.response_class(
        response=json.dumps("Unknown key"),
        status=400,
        mimetype='application/json'
    )





    if result == -1:  # if can't get location from memcache, get location from DB
        DBresult = BackendApp.db.get_image_with_key(key) # method from db to get image location using specific key
        if DBresult is None:
            return response
        else:
            #flash("We can't find the file from cache but we found it in database, and we restore it back to cache ")
            fname = os.path.join('app/static/images', key)
            with open(fname, "rb") as image_file:
                encoded_image = b64encode(image_file.read()).decode('utf-8')

            if memcache.put(key, encoded_image):
                # add the key and file name to cache as well as database
                print(memcache.getSpace())
                #memcache.put(key,fname)#save current request to memcache
                return render_template("display_image.html", result = fname[4:])#return image address
            else:
                response1 = webapp.response_class(
                    response=json.dumps("We can't find the file from cache and we found it in database,the size of the restore image exceed the maximum capacity."),
                    status=400,
                    mimetype='application/json'
                )
                return response1
        return response
    else:
        #decode base64 string data
        #decoded_image = base64.b64decode(result)

        return render_template("display_image_cache.html", image=result)


@webapp.route('/upload', methods=['POST'])
def upload():

    key = request.form.get('key')

    new_image = request.files['file']
    fname = os.path.join('app/static/images', key)
    new_image.save(fname)

    with open(fname, "rb") as image_file:
        encoded_image = b64encode(image_file.read()).decode('utf-8')
    print('Image size: ', sys.getsizeof(encoded_image))
    print('Cache Cap: ', memcache.getCap())

    if memcache.put(key, encoded_image):
        #print('Image size: ', sys.getsizeof(encoded_image))
        #print('Cache Cap: ', memcache.getCap())
    #memcache.put(key, encoded_image)  # add the key and file name to cache as well as database

        BackendApp.db.put_image(key,fname,'app/static/images') # method from db to put image


        response = webapp.response_class(
            response=json.dumps("OK"),
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        response1 = webapp.response_class(
            response=json.dumps("The size of the image is larger than the capacity of the cache"),
            status=400,
            mimetype='application/json'
        )
        return response1




