from app import *

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE student_contact = %s AND student_password= %s', (username, password))
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            # global session
            session['loggedin'] = True
            session['username'] = account['student_contact']
            session['user_type'] = 'student'
            session['id'] = account['student_id']
            session['grade'] = account['student_grade']
            return redirect(url_for('home',num=1))
        else:
            flash("Invalid Username or Password !")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout/')
def logout():
    print('hi')
    # Remove session data, this will log the user out
    session.pop('loggedin', None)

    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))
