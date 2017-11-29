from flask import Flask, redirect, url_for, \
				  request, render_template, json
from pymongo import MongoClient
import pymongo
import os
import socket
from bson import ObjectId



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


client = MongoClient('mongodb://backend:27017/dockerdemo')
db = client.blogpostDB

app = Flask(__name__)

@app.route("/")
def landing_page():
    posts = get_all_posts()
    
    return render_template('blog.html', posts=json.loads(posts))

@app.route('/add_post', methods=['POST'])
def add_post():

    new()
    return redirect(url_for('landing_page'))



@app.route('/remove_post', methods=['POST'])
def remove_post():

    remove()
    return redirect(url_for('landing_page'))


@app.route('/update_post')
def update_post():
    print "update"
    return render_template('edit_blog.html', post=json.loads(get_post()))


@app.route('/get_post', methods=['GET'])
def get_post():
    return JSONEncoder().encode(get_posts({"_id": ObjectId(request.args["id"])}))


@app.route('/remove_all')
def remove_all():
    db.blogpostDB.delete_many({})

    return redirect(url_for('landing_page'))


@app.route('/edit_post', methods=['POST'])
def edit_post():

    update()
    return redirect(url_for('landing_page'))



## Services

@app.route("/posts", methods=['GET'])
def get_all_posts():

    return JSONEncoder().encode(get_posts())


@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'title': request.form['title'],
        'post': request.form['post']
    }

    db.blogpostDB.insert_one(item_doc)

    posts = get_posts()
    return JSONEncoder().encode(posts[-1])


### Insert function here ###


def remove():
    id = request.form['id']

    db.blogpostDB.delete_one({'_id': ObjectId(id)})

    return JSONEncoder().encode(get_posts())

def get_posts(query = {}):
    _posts = db.blogpostDB.find(query)
    return [post for post in _posts]

def update():
    id = request.form['id']

    item_doc = {
        'title': request.form['title'],
        'post': request.form['post']
    }

    db.blogpostDB.update_one({"_id": ObjectId(id)}, { "$set": item_doc })

    return JSONEncoder().encode(get_posts())

############################



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
