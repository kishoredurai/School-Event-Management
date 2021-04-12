from app import *

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)








        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE student_contact = %s AND student_password= %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        pro = []

        if account:
            # Create session data, we can access this data in other routes
            # global session
            session['loggedin'] = True

            session['username'] = account['student_contact']
            session['password'] = account['student_password']
            session['grade'] = account['student_grade']

            # if session
            # Redirect to home page


            # for i in range(len(course)):
            #   print(course[i]['course_id'])
            #  print(course[i]['course_name'])

            return redirect(url_for('home',num=1))

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('students/index.html', msg=msg)

@app.route('/logout/')
def logout():
    print('hi')
    # Remove session data, this will log the user out
    session.pop('loggedin', None)

    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))
