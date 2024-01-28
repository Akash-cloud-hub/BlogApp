from flask import Flask , redirect , url_for , render_template , session , flash
from datetime import *
import math
import json
import utility

import pyodbc

app = Flask(__name__)
def connectToDb():
    with open('config.json',"r") as c:
        conString = json.load(c)['connectionString']['BlogApp']

    # # Replace these values with your actual server and database information
    # server_name = config_param['server_name']
    # database_name = config_param['database_name']

    # Construct the connection string
    connection_string = conString

    # Connect to the database
    cnxn = pyodbc.connect(connection_string)

    cursor = cnxn.cursor()
    return cursor

def performCRUD(query):
    cursor = connectToDb()
    records = cursor.execute(query)
    list_of_records = utility.fetch_data_as_list_of_dicts(records)
    # print(users)
    return list_of_records

@app.route('/')
def home():
    post = performCRUD("Select * From Posts")
    # print(post)
    return render_template("post.html",post = post)

@app.route('/post/<slug>', methods = ['GET'])
def post(slug):
    print(slug)
    singlePost = performCRUD(f"Select * From Posts Where Slug = '{slug}' ")[0]
    print(singlePost)
    return render_template("post.html", post = singlePost)

@app.route('/login')
def login():
    return "login"

@app.route('/about')
def about():
    return "about"

@app.route('/contact')
def contact():
    return "post"


if __name__ == '__main__':
#     cursor = connectToDb()
    app.run(debug=True)