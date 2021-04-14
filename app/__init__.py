from flask import Flask, render_template, request, redirect, url_for, session,Response,flash
import MySQLdb.cursors
import re
import moviepy.editor
from flask_mail import Mail, Message
from flask_mysqldb import MySQL
from authy.api import AuthyApiClient
import mysql.connector
from mysql import connector
import rsa

publicKey, privateKey = rsa.newkeys(512)


app = Flask(__name__)
mysql = MySQL(app)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = '121.200.55.42'
app.config['MYSQL_PORT'] = 4063
app.config['MYSQL_USER'] = 'cloud'
app.config['MYSQL_PASSWORD'] = 'cloud@123'
app.config['MYSQL_DB'] = 'elearning'

mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ssig432@gmail.com'
app.config['MAIL_PASSWORD'] = 'Ssig@1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

app.secret_key = '11sdcasd'


api = AuthyApiClient('F79FjHOmziWHkVTBA9K6MgqUvKww3qui')





from app.code import login_logout,student,forgetpassword,signup