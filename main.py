from flask import Flask , redirect , url_for , render_template , session , flash , request
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
    # list_of_records = utility.fetch_data_as_list_of_dicts(records)
    # print(users)
    return records

@app.route('/')
def home():
    records = performCRUD("Select * From Posts")
    post = utility.fetch_data_as_list_of_dicts(records)

    # print(post)
    return render_template("post.html",post = post)

@app.route('/post/<slug>', methods = ['GET'])
def post(slug):
    print(slug)
    records = performCRUD(f"Select * From Posts Where Slug = '{slug}' ")
    singlePost = utility.fetch_data_as_list_of_dicts(records)[0]

    print(singlePost)
    return render_template("post.html", post = singlePost)



@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/signup',methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        NameOfUser = request.form.get('NameOfUser')
        Email = request.form.get('Email')
        UserName = request.form.get('UserName')
        Password = request.form.get('Password')

        records = performCRUD(f"Select * From Users Where Email = '{Email}' ")
        user = utility.fetch_data_as_list_of_dicts(records)
        if user:
            flash('Email address already exists')
            return redirect(url_for('signup'))

        query = f'''INSERT INTO [Users]
( 
 [NameOfUser], [Email], [UserName],[Password]
)
VALUES
( 
 '{NameOfUser}', '{Email}', '{UserName}','{Password}'
)'''
        print(query)
        result = performCRUD(query)
        result.commit()
        print(result)
        result.close()

        return redirect(url_for('login'))
    return render_template("signup.html")

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        UserName = request.form.get('UserName')
        Password = request.form.get('Password')
        records = performCRUD(f"Select * From Users Where UserName = '{UserName}' and Password='{Password}' ")
        user = utility.fetch_data_as_list_of_dicts(records)
    return "login"

@app.route('/contact')
def contact():
    return "post"


if __name__ == '__main__':
#     cursor = connectToDb()
    app.run(debug=True)