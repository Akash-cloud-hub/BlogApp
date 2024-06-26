import datetime

from flask import Flask , redirect , url_for , render_template , session , flash , request
from datetime import *
import math
import json
import utility
import os


import re

import pyodbc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this_is_the_secret_key'

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
    cursor = cursor.execute(query)
    # list_of_records = utility.fetch_data_as_list_of_dicts(records)
    # print(users)
    return cursor

def authorize_user(UserId):
    records = performCRUD(
        f"Select UserId , NameOfUser  From Users Where UserId = '{UserId}' ")
    user = utility.fetch_data_as_list_of_dicts(records)
    if user:
        return True
    else:
        return False

@app.route('/')
def home():
    # records = performCRUD("Select * From Posts")
    # post = utility.fetch_data_as_list_of_dicts(records)

    # Check if 'username' is in session
    if 'UserId' in session:
        return redirect(url_for('postlibrary'))

    return redirect(url_for('login'))

@app.route('/posts',methods=['GET'])
def posts():
    UserId = session.get('UserId')

    is_user_authorized = False
    if UserId:
        is_user_authorized = authorize_user(UserId)

    if is_user_authorized:
        records = performCRUD(f"Select * From Posts ")
        posts = utility.fetch_data_as_list_of_dicts(records)

        print(posts)
        return render_template("post.html", post=posts)
    else:
        return redirect(url_for('home'))




@app.route("/Library/",methods=['GET'])
def postlibrary():
    search_text = request.args.get('search_text','All')
    if request.method == 'GET':
        print(search_text)
        query = f""" Select * From Posts where ( '{search_text}' = 'All' 
        or Content1 like '%{search_text}%'
         or Title like '%{search_text}%' )"""
        print(query)
        records = performCRUD(query)
        posts = utility.fetch_data_as_list_of_dicts(records)
        for i in range(len(posts)):
            posts[i]['SRNO'] = i+1

        print(posts)
        n = 4
        last = math.ceil(len(posts)/n)
        page = request.args.get('page')
        print('page:' , page)
        if not str(page).isnumeric():
            page = 1
        page = int(page)
        j = (page-1) * n

        posts = posts[j:j+n]
        print("Sliced Posts : ")
        print(posts)


        if page == 1:
            prev = '/?page=' + str(last) + '&' + f'?search_text={search_text}'
            next = '/?page=' + str(page+1) + '&' + f'?search_text={search_text}'
        elif page == last:
            prev = '/?page=' + str(page-1) + '&' + f'?search_text={search_text}'
            next = '#'
        else:
            prev = '/?page=' + str(page-1) + '&' + f'?search_text={search_text}'
            next = '/?page=' + str(page + 1) + '&' + f'?search_text={search_text}'


        return render_template('library_posts.html' , posts = posts , prev = prev , next = next , NameOfUser = session.get('NameOfUser'))
    else:
        error = {'error_message': 'Request failed , please make a Get Request ! ' }
        return render_template('error.html', error=error)


@app.route('/post/<slug>', methods = ['GET'])
def post(slug):
    print(slug)
    UserId = session.get('UserId')

    is_user_authorized = False
    if UserId:
        is_user_authorized = authorize_user(UserId)

    if is_user_authorized:
        records = performCRUD(f"Select * From Posts Where Slug = '{slug}' ")
        singlePost = utility.fetch_data_as_list_of_dicts(records)[0]

        print(singlePost)
        return render_template("post.html", post = singlePost)
    else:
        return redirect(url_for('home'))



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
        records = performCRUD(f"Select UserId , NameOfUser , UserRole  From Users Where UserName = '{UserName}' and Password='{Password}' ")
        user = utility.fetch_data_as_list_of_dicts(records)

        print(user)

        session['NameOfUser'] = user[0]['NameOfUser']
        # session['UserName'] = user[0]['UserName']
        session['UserId'] = user[0]['UserId']
        session['UserRole'] = user[0]['UserRole']

        print(records)
        if user:
            print("home")
            return redirect(url_for('home'))
        else:
            flash("Password or username is incorrect , please try again !")
            # return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

UPLOAD_FOLDER = 'static/images/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/create_post',methods=['POST','GET'])
def create_post():

    if request.method=='POST':
        data = {}
        try:
            data = dict(request.form)
            data['DatePosted'] = utility.format_datetime(data.get('DatePosted'))
            if 'Image' not in request.files:
                return "No file part"
            file = request.files['Image']
            if file.filename == '':
                return 'No selected file'
            if file:
                filename = file.filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                data['Image'] = f'images/img/{filename}'
        except Exception as e:
            print(e)
            return "There has been an error creating the post, please try again!"

        print(data)
        query = f'''
            INSERT INTO [Posts]
            ( 
                    [Title]
                  ,[Subtitle]
                  ,[Location]
                  ,[Author]
                  ,[DatePosted]
                  ,[Image]
                  ,[Content1]
                  ,[Content2]
                  ,[Slug]
            )
            VALUES
            ( 
                    '{data.get('Title')}'
                  ,'{data.get('Subtitle')}'
                  ,'{data.get('Location')}'
                  ,'{data.get('Author')}'
                  ,'{data.get('DatePosted')}'
                  ,'{data.get('Image')}'
                  ,'{data.get('Content1')}'
                  ,'{data.get('Content2')}'
                  ,'{data.get('Slug')}'
            )
                    '''
        print(query)

        cursor = performCRUD(query)
        cursor.commit()
        print(cursor)

        return redirect(url_for('post',slug = data.get('Slug')))

    return render_template('create_post.html',action='create_post',actionPost = '/create_post',buttonText = 'Create Post')


# @app.route('/')
# def index():
#     # Check if 'username' is in session
#     if 'UserName' in session:
#         return 'Logged in as ' + session['UserName'] + '<br>' + \
#                "<b><a href = '/logout'>click here to log out</a></b>"
#     return "You are not logged in <br><a href = '/login'></b>" + \
#            "click here to log in</b></a>"

@app.route('/contact',methods=['POST' , 'GET'])
def contact():
    if request.method == 'POST':
        data = {}
        data = dict(request.form)
        contact = {
            'Name': data.get('Name'),
            'Email': data.get('Email'),
            'Message': data.get('Message'),
            'CreatedOnDate': data.get('CreatedOnDate'),
            'IsActive': 1,  # in SQL true = 1
            'InstagramLink': data.get('InstagramLink'),
            'TwitterLink': data.get('TwitterLink')
        }
        insert_query = utility.generate_insert_query("ContactInformation",contact)
        print(insert_query)
        cursor = performCRUD(insert_query)
        cursor.commit()
        cursor.close()
        return "We will get in touch with you soon . "

    return render_template('contact.html')

@app.route("/editPost/<int:PostId>",methods=['GET','POST'])
def editContact(PostId):
    query = f"""
                    SELECT [po].[PostId],
                    [po].[Title],
                    [po].[Subtitle],
                    [po].[Location],
                    [po].[Author],
                    [po].[DatePosted],
                    [po].[Image],
                    [po].[Content1],
                    [po].[Content2],
                    [po].[Slug],
                    [po].[UserId],
                    [us].[UserRole] FROM [dbo].[Posts] po 
                        left JOIN dbo.Users us 
                        ON po.UserId=us.UserId
                    WHERE po.PostId = '{PostId}' """

    records = performCRUD(query)
    post = utility.fetch_data_as_list_of_dicts(records)
    print("The requested information from post : ")
    print(post)
    if request.method == 'POST':
        LoggedInUserId = session['UserId']
        role = post[0].get('UserRole')
        if role =='Admin' or LoggedInUserId == post[0].get('UserId'):
            print("Admin trying to edit...")
            data = {}
            data = dict(request.form)

            data['DatePosted'] = utility.format_datetime(data.get('DatePosted','2024-01-04 00:00:00.000'))
            updateQuery = f"""
                    UPDATE [dbo].[Posts]
                SET 
                    [Title] = '{data.get('Title','Null')}',
                    [Subtitle] = '{data.get('Subtitle','Null')}',
                    [Location] = '{data.get('Location','Null')}',
                    [Author] = '{data.get('Author','Null')}',
                    [DatePosted] = '{data.get('DatePosted',f'{datetime.now()}')}',
                    [Image] = '{data.get('Image','Null')}',
                    [Content1] = '{data.get('Content1','Null')}',
                    [Content2] = '{data.get('Content2','Null')}',
                    [Slug] = '{data.get('Slug','Null')}'
                WHERE
                    [PostId] = '{PostId}'"""
            print(updateQuery)
            cursor = performCRUD(updateQuery)
            cursor.commit()

    return render_template('create_post.html', action= 'editing' , actionPost=f'/editPost/{int(PostId)}'
                           , buttonText='Update Post', post = post[0] )


@app.route("/deletePost/<int:PostId>",methods=['GET','POST'])
def deletePost(PostId):
    if request.method == 'POST':
        query = f"""DELETE FROM [dbo].[Posts]
                    WHERE PostId = {PostId}"""
        cursor = performCRUD(query)
        cursor.commit()
        return "deleted..."
    return redirect(url_for('admin'))

@app.route('/admin',methods=['GET'])
def admin():
    print(session)
    userRole = session['UserRole']
    if userRole == 'Admin':
        records = performCRUD(f"Select PostId , Title From Posts")
        post = utility.fetch_data_as_list_of_dicts(records)
        contact_list = performCRUD(f"Select ContactInformationId , Name , Email  From ContactInformation")
        contacts = utility.fetch_data_as_list_of_dicts(contact_list)
        return render_template('/admin/index.html',posts = post , contacts = contacts)
    else:
        return 404,'Not Found'

if __name__ == '__main__':
#     cursor = connectToDb()
    app.run(debug=True)