
from app import *





@app.route("/")
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
            return redirect(url_for('home'))
        else:
            flash("Invalid Username or Password !")
            return redirect(url_for('login'))

    if(not session.get("id") is None):
        if(session.get("user_type") == 'student'):
            return redirect(url_for('home'))
        elif(session.get("user_type") == 'provider'):
            return redirect(url_for('provider_home'))
        else:
            session.pop("id", None)
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout/')
def logout():
    # Remove session data, this will log the user out
    session.clear()

    # Redirect to login page
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):

    app.logger.info(f"Page not found: {request.url}")

    return redirect(url_for('login'))
