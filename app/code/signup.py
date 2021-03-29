from app import *
@app.route('/studentreg', methods=['GET', 'POST'])
def studentreg():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'mno' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        grade=request.form['grade']
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
            cursor.execute('INSERT INTO students VALUES ( %s, %s, %s,%s, %s, %s,%s)',
                           (mno,password,username,sname,city,state,grade))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return render_template('students/index.html',msg=msg)
