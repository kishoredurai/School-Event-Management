from app import  *
@app.route('/home', methods=['GET', 'POST'])


def home():
    if 'username' in session:
        username = session['username']
        pas=session['password']

        print(username)





        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM students WHERE mno = %s AND pass= %s', (username, pas))
        # Fetch one record and return result
        account = cursor.fetchone()


        cursor.execute('SELECT course_id,course_name FROM course WHERE stan = %s', (account['grade']))
        course = cursor.fetchall()



        return render_template('students/home.html', res=account, course=course, len=len(course),b=account['grade'])
    else:
        return redirect(url_for('login'))

@app.route("/get_course", methods=["GET", "POST"])
def get_course():
    if 'username' in session:
        a = request.args.get('a')
        b= request.args.get('b')
        print(a)
        print(b)




        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('Select * from subcourse where grade=%s and sub=%s ', [b, a])
        course1 = cursor.fetchall()
        print(course1)
        cursor.execute('SELECT course_id,course_name FROM course WHERE stan = %s', (b))
        course = cursor.fetchall()
        session['loggedin'] = False
        return render_template('students/subcourse.html',course1=course1,course=course,len1=len(course1),len=len(course),b=b)
    else:
        return redirect(url_for('login'))
        
        



@app.route("/video", methods=["GET", "POST"])
def video():
    if 'username' in session:
        s = request.args.get('s')
        n = int(s)

        c = request.args.get('c')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM video WHERE sub_cid  = %s', (c,))
        vid = cursor.fetchall()

        print(vid[0]['link'])
        cursor.execute('SELECT course_id,course_name FROM course WHERE stan = %s', (session['grade']))
        course = cursor.fetchall()

        return render_template('students/video.html', vid=vid[n], len2=len(vid), n=n, course=course, len=len(course),
                               b=session['grade'])
    else:
        return redirect(url_for('login'))
        
        

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if 'username' in session:

        username = session['username']
        grade=session['grade']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM students WHERE mno  = %s', (username,))
        account = cursor.fetchone()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT course_id,course_name FROM course WHERE stan = %s', (grade))
        course = cursor.fetchall()
        b=account['grade']


        return render_template('students/student_profile.html',name=account,course=course,len=len(course),b=b)
    else:
        return redirect(url_for('login'))
        
        
@app.route("/changepwd", methods=["GET", "POST"])
def changepwd():
        msg=''
        if request.method == "POST":
            passwd = request.form.get("confirm_password")

            phone_number = session.get("username")
            print(phone_number)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE students set pass=%s where mno=%s', [passwd,phone_number])
            mysql.connection.commit()
            msg="Password changed successfully !!!"
            return render_template('students/password.html',msg=msg)
        return render_template('password.html')