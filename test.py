from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sem'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('i.html')
@app.route('/success', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        mno = details['mno']
        name = details['name']
        city = details['city']
        school = details['school']
        state = details['state']
        pwd = details['pwd']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students(mno,stname,scname,city,state,pass) VALUES (%s,%s,%s,%s,%s,%s)", (mno,name,city,school,state,pwd))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('i.html')


if __name__ == '__main__':
    app.run()