from app import *
@app.route('/studentreg', methods=['GET', 'POST'])
def studentreg():
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'fname' in request.form and 'password' in request.form and 'mno' in request.form:
        # Create variables for easy access
        fname = request.form['fname']
        lname = request.form['lname']
        date=request.form['date']
        gender = request.form['gender']
        grade = int(request.form['grade'])
        sname=request.form['sname']
        password = request.form['password']


        mno = request.form['mno']
        add = request.form['add']
        city = request.form['city']
        state = request.form['state']
        pin= int(request.form['pin'])
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE student_contact  = %s', (mno,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'

        elif not re.match(r'[A-Za-z0-9]+', fname):
            msg = 'Username must contain only characters and numbers!'
        elif not password or not mno:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO student (student_Fname, student_Lname, student_dob, student_gender,student_grade,student_school,student_password,student_contact,student_address,student_add_district,student_add_state,student_add_pincode)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(fname,lname,date,gender,grade,sname,password,mno,add,city,state,pin))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return render_template('students/index.html',msg=msg)
