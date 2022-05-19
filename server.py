import json
from re import X
from this import d
from typing import Hashable
from flask import Flask, request, jsonify
from datetime import datetime
from sqlite3 import Connection as SQLite3Connection
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_sqlalchemy import  SQLAlchemy
import random

import linked_list
import hash_table
import bst
import queue
import stack


#app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

# configure SQLite3 to enforce foreign key constraints
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
  if isinstance(dbapi_connection, SQLite3Connection):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

# connect DB ORM to flask app
db = SQLAlchemy(app)
now = datetime.now()

# models
class User(db.Model):
  __tablename__ = "user"
  id = db.Column(db.Integer, primary_key= True)
  name = db.Column(db.String(25))
  email = db.Column(db.String(25))
  address = db.Column(db.String(50))
  phone = db.Column(db.String(10))
  posts = db.relationship("BlogPost", cascade= "all, delete")

class BlogPost(db.Model):
  __tablename__ = "blog_post"
  id = db.Column(db.Integer, primary_key= True)
  title = db.Column(db.String(25))
  body = db.Column(db.String(200))
  date = db.Column(db.Date)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable= False)

 # routes
@app.route("/user", methods= ["POST"])
def create_user():
  # parse incoming request as json
  data = request.get_json()
  new_user = User(
  name = data["name"],
  email = data["email"],
  address = data["address"],
  phone = data["phone"]
  )
  db.session.add(new_user)
  db.session.commit()
  return jsonify({"message":"User created"}), 200

@app.route("/user/descending_id", methods= ["GET"])
def get_all_users_descending():
  users = User.query.all()
  users_ll = linked_list.LinkedList()

  for user in users:
    users_ll.insert_beginning(
      {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "address": user.address,
        "phone": user.phone
      }
    )
  return jsonify(users_ll.to_arr()), 200

@app.route("/user/ascending_id", methods= ["GET"])
def get_all_users_ascending():
  users = User.query.all()
  users_ll = linked_list.LinkedList()

  for user in users:
    users_ll.insert_ending(
      {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "address": user.address,
        "phone": user.phone
      }
    )
  return jsonify(users_ll.to_arr()), 200

@app.route("/user/<user_id>", methods= ["GET"])
def get_one_user(user_id):
  users = User.query.all()
  users_ll = linked_list.LinkedList()

  for user in users:
    users_ll.insert_ending(
      {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "address": user.address,
        "phone": user.phone
      }
    )
  user = users_ll.get_user_id(user_id)
  return jsonify(user), 200

@app.route("/user/<user_id>", methods= ["DELETE"])
def delete_user(user_id):
  user = User.query.filter_by(id= user_id).first()
  db.session.delete(user)
  db.session.commit()
  op = f"deleted user_id {user_id}"
  return jsonify(op), 200

@app.route("/blog_post/<user_id>", methods= ["POST"])
def create_blog_post(user_id):
  data = request.get_json()

  # check if user_id passed in request exists in Users table
  user = User.query.filter_by(id=user_id)
  if not user: 
    return jsonify({"message": "User does not exist"}), 404

  ht = hash_table.HashTable(10)

  ht.add_key_value("title", data["title"])
  ht.add_key_value("body", data["body"])
  ht.add_key_value("date", now)
  ht.add_key_value("user_id", user_id)

  ht.print_table()
  ht.get_value("date") 

  new_blog = BlogPost(
    title = ht.get_value("title"),
    body = ht.get_value("body"),
    date = ht.get_value("date"),  
    user_id = ht.get_value("user_id")
  )

  db.session.add(new_blog)
  db.session.commit()

  ts = ht.get_value("date")
  return jsonify(f"Created post at {ts} "), 200

@app.route("/blog_post/<blog_post_id>", methods= ["GET"])
def get_one_blog_posts(blog_post_id):
  blog_posts = BlogPost.query.all()
  random.shuffle(blog_posts)

  blog_tree = bst.BinarySearchTree()

  for post in blog_posts:
    blog_tree.insert(
      {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "user_id": post.user_id

      }
    )

  post = blog_tree.search(blog_post_id)

  if not post:
    return jsonify("Post not found"), 404

  return jsonify(post), 200

@app.route("/blog_post/numeric_body", methods= ["GET"])
def get_numeric_post_bodies():
  blog_posts = BlogPost.query.all()
  q = queue.Queue()
  print(f'{len(blog_posts)} blog posts fetched')

  for post in blog_posts:
    q.enqueue(post)

  return_list = []

  # for _ in range(len(blog_posts)):
  #   post = q.dequeue()
    # print(post.data.body)
    # numeric_body = 0
    # for char in post.data.body:
    #   numeric_body += ord(char)
    # post.data.body = numeric_body
    # return_list.append(
    #   { 
    #     "id": post.data.id
    #     # "title": post.data.title,
    #     # "body": post.data.body,
    #     # "user_id": post.data.user_id 
    #   })
  return jsonify(str(q)), 200
  

@app.route("/blog_post/delete_last_10", methods= ["DELETE"])
def delete_last_10():
  blog_posts = BlogPost.query.all()

  s = stack.Stack()

  for post in blog_posts:
    s.push(post)

  for _ in range(10):
    post_to_delete = s.pop()
    db.session.delete(post_to_delete.data)
    db.session.commit()

  return jsonify({"message": "Last 10 posts deleted"}), 200

    
if __name__ == "__main__":
  app.run(debug= True)