from flask import Flask,render_template,url_for,request
from flask_mail import Mail, Message
from flask_mysqldb import MySQL
import MySQLdb.cursors
app = Flask(__name__)
mail = Mail(app)  # instantiate the mail class
mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'barathg'
app.config['MYSQL_DB'] = 'sem'

# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ssig432@gmail.com'
app.config['MAIL_PASSWORD'] = 'Ssig@1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# message object mapped to a particular URL ‘/’
@app.route("/")
def home():
    return render_template('auth.html')
@app.route("/test/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        details = request.form
        ma = str(details['mail'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            'SELECT * FROM email WHERE ename= %s ',[ma])
        account = cursor.fetchone()

        if account:

            msg = Message(
                'Hello',
                sender='ssig432@gmail.com',
                recipients=[ma]
            )
            print(mail)
            msg.body = 'Hello Flask message sent from Flask-Mail'
            mail.send(msg)
            return 'Sent'
        else:
            return 'failed'


if __name__ == '__main__':
    app.run(debug=True)