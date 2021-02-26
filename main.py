from flask import Flask, render_template, request, redirect, url_for, session,Response
from flask_mysqldb import MySQL
from authy.api import AuthyApiClient
import MySQLdb.cursors
import re
from flask_mail import Mail, Message
import datetime
import mysql.connector
from config import *

app = Flask(__name__)
mail = Mail(app)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'barathg'
app.config['MYSQL_DB'] = 'sem'

mysql = MySQL(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ssig432@gmail.com'
app.config['MAIL_PASSWORD'] = 'Ssig@1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']


api = AuthyApiClient(app.config['AUTHY_API_KEY'])

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM students WHERE mno = %s AND pass= %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()

        if account:
            # Create session data, we can access this data in other routes
            # global session
            session['loggedin'] = True

            session['username'] = account['mno']

            #if session
            # Redirect to home page

            return redirect(url_for('home'))

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'


    return render_template('index.html',msg=msg)


@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' in session:
        username = session['username']
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


@app.route('/login/teach', methods=['GET', 'POST'])
def login_tech():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            'SELECT * FROM teachers,others WHERE teachers.email= %s AND teachers.pass= %s OR others.email= %s AND others.pass= %s ',
            (username, password, username, password))
        # Fetch one record and return result
        account = cursor.fetchone()

        if account:

            # Create session data, we can access this data in other routes
            # global session
            session['loggedin'] = True

            session['username'] = account['email']
            # Redirect to home page

            return redirect(url_for('home'))

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('index_tec.html', msg=msg)
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        sname = request.form['sname']
        mno= request.form['mno']
        city = request.form['city']
        state = request.form['state']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM teachers WHERE email  = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO teachers VALUES ( %s, %s, %s,%s, %s, %s,%s)', ( email,username,mno,sname,city,state,password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/registeroth', methods=['GET', 'POST'])
def registeroth():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        add = request.form['add']
        mno = request.form['mno']
        city = request.form['city']
        state = request.form['state']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM others WHERE email  = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO others VALUES ( %s, %s, %s,%s, %s, %s,%s)',
                           (email, username, mno, add, city, state, password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return render_template('registeroth.html',msg=msg)


@app.route('/studentreg', methods=['GET', 'POST'])
def studentreg():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'mno' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        sname = request.form['sname']
        mno = request.form['mno']
        city = request.form['city']
        state = request.form['state']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM students WHERE mno  = %s', (mno,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'

        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not mno:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO students VALUES ( %s, %s, %s,%s, %s, %s)',
                           (mno,password,username,sname,city,state))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return render_template('studentreg.html',msg=msg)

@app.route('/logout/')
def logout():
    print('hi')
    # Remove session data, this will log the user out
    session.pop('loggedin', None)

    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route("/verification", methods=["GET", "POST"])
def verification():
    if request.method == "POST":
        country_code = "+91"
        phone_number = request.form.get("phone_number")
        method = "sms"

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            'SELECT * FROM students WHERE mno= %s ', [phone_number])
        account = cursor.fetchone()

        cursor.execute(
            'SELECT * FROM teachers WHERE email= %s ', [phone_number])
        account1 = cursor.fetchone()

        if account:
            session['country_code'] = country_code
            session['phone_number'] = phone_number

            api.phones.verification_start(phone_number, country_code, via=method)
            return redirect(url_for("verify"))

        if account1:

            session['country_code'] = country_code
            session['phone_number'] = phone_number

            msg = Message(
                'Hello',
                sender='ssig432@gmail.com',
                recipients=[phone_number]
            )
            print(mail)
            msg.body = 'http://127.0.0.1:5000/passwdemail/' + phone_number
            mail.send(msg)

            return Response("<h1>Mail Sent Successfully!</h1>")

        else:
            return Response("<h1>Failes!</h1>")

    return render_template("verification.html")


@app.route("/passwdemail/<name>")
def passwdemail(name):
        session['emailid'] = name
        return redirect(url_for("emailpasswd"))

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
            token = request.form.get("token")

            phone_number = session.get("phone_number")
            country_code = session.get("country_code")

            if phone_number=='':
                return render_template("changepwd.html")


            verification = api.phones.verification_check(phone_number,
                                                         country_code,
                                                         token)

            if verification.ok():
                return render_template("changepwd.html")
                # return Response("<h1>Success!</h1>")

    return render_template("verify.html")

@app.route("/emailpasswd", methods=["GET", "POST"])
def emailpasswd():
    email = session.get("emailid")
    if request.method == "POST":
        passwd = request.form.get("epasswd")
        email = session.get("emailid")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE teachers set pass=%s where email=%s',[passwd,email])
        mysql.connection.commit()
        return Response("<h1>Success!</h1>")
        #return Response("<h1>"+email+"</h1>")

    return render_template("emailpasswd.html")

@app.route("/changepwd", methods=["GET", "POST"])
def changepwd():
        if request.method == "POST":
            passwd = request.form.get("passwd")

            phone_number = session.get("phone_number")
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE students set pass=%s where mno=%s', [passwd,phone_number])
            mysql.connection.commit()
            return Response("<h1>Success!</h1>")


if __name__ == "__main__":
    app.run(debug=True)