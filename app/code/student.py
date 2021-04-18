from app import  *

@app.route('/home', methods=["GET", "POST"])
def home():
    if 'username' in session and session.get("user_type") == 'student':
        stu_id=session.get('id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE student_id = %s',[stu_id])
        account = cursor.fetchone()
        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s',[account['student_grade']])
        subject = cursor.fetchall()
        return render_template('students/student_home.html', res=account, subject=subject, len=len(subject),b=account['student_grade'])
    else:
        return redirect(url_for('login'))

@app.route("/get_course", methods=["GET", "POST"])
def get_course():
    if 'username' in session:
        username = session['username']
        a = request.args.get('a')
        b= request.args.get('b')
        c = request.args.get('c')
        print(a)
        print(b)




        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('Select * from course where course_grade=%s and subject_id=%s ', [b, a])
        course1 = cursor.fetchall()
        print(course1)
        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s', (b))
        subject = cursor.fetchall()
        cursor.execute('SELECT * FROM student WHERE student_contact  = %s', (username,))
        account = cursor.fetchone()
        session['loggedin'] = False
        return render_template('students/subcourse.html',course1=course1,res=account,subject=subject,len1=len(course1),len=len(subject),b=b,c=c)
    else:
        return redirect(url_for('login'))
        
        



@app.route("/sub_content", methods=["GET", "POST"])
def sub_content():
    if 'username' in session:
        username = session['username']


        c = request.args.get('c')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE student_contact  = %s', (username,))
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM course_chapter WHERE course_id  = %s', (c,))
        vid = cursor.fetchall()

        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s',(session['grade'],))
        subject = cursor.fetchall()

        return render_template('students/subject_content.html',res=account, vid=vid,len2=len(vid), subject=subject, len=len(subject),
                               b=session['grade'])
    else:
        return redirect(url_for('login'))

@app.route("/video", methods=["GET", "POST"])
def video():
    if 'username' in session:
        username = session['username']
        s=request.args.get('s')
        print(s)
        if s==None:
            n=0
        else:
            n=int(s)
            print(n)

        c = request.args.get('c')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE student_contact  = %s', (username,))
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM content_video,course_chapter_content where content_video.chapter_content_id = course_chapter_content.chapter_content_id and course_chapter_content.course_chapter_id =%s ', (c,))
        content = cursor.fetchall()
        print(content)



        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s',(session['grade'],))
        subject = cursor.fetchall()

        return render_template('students/video.html', content=content[n],res=account, len2=len(content), n=n, subject=subject, len=len(subject),
                               b=session['grade'])
    else:
        return redirect(url_for('login'))
        
        

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if 'username' in session:
        sa = request.args.get('sa')

        username = session['username']
        grade=session['grade']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE student_contact  = %s', (username,))
        account = cursor.fetchone()
        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s',(session['grade'],))
        subject = cursor.fetchall()




        return render_template('students/student_profile.html', res=account, subject=subject, len=len(subject),b=grade,sweetalert=sa)
    else:
        return redirect(url_for('login'))
        

@app.route("/update", methods=["GET", "POST"])
def update():
    if 'username' in session and request.method == 'POST':
        username = session['username']
        grade = session['grade']
        fname = request.form['first_name']
        lname = request.form['last_name']
        sname=request.form['s_name']
        dob=request.form['dob']
        add = request.form['address']
        city = request.form['city']
        state = request.form['state']


        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('update student set student_Fname= %s, student_Lname=%s , student_school=%s, student_dob=%s , student_address=%s, student_add_district=%s,student_add_state=%s where student_contact=%s', (fname,lname,sname,dob,add,city,state,username))
        mysql.connection.commit()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE student_contact  = %s', (username,))
        account = cursor.fetchone()
        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s',(session['grade'],))
        subject = cursor.fetchall()

        return redirect(url_for('profile',sa=1))
    else:
        return redirect(url_for('login'))


@app.route('/change_profile_image', methods = ['POST'])
def change_profile_image():
    if 'username' in session and request.method == 'POST':
        username = session['username']

        f = request.files['file']
        filename = secure_filename(f.filename)
        path="static/img/profile_image/{0}".format(filename)
        f.save(os.path.join(app.root_path, path))
        path1="img/profile_image/{0}".format(filename)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('update student set student_profile_image=%s WHERE student_contact  = %s', (path1,username,))
        mysql.connection.commit()
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))


@app.route('/test')
def test():
    return render_template('students/course_enroll.html')

#@app.route('/enroll_course',method=['POST'])
#def enroll_course():
 #   if 'username' in session and request.method == 'POST':

  #      return 'c'












# @app.route("/changepwd", methods=["GET", "POST"])
# def changepwd():
#         msg=''
#         if request.method == "POST":
#             passwd = request.form.get("confirm_password")

#             phone_number = session.get("username")
#             print(phone_number)
#             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             cursor.execute('UPDATE students set pass=%s where mno=%s', [passwd,phone_number])
#             mysql.connection.commit()
#             msg="Password changed successfully !!!"
#             return render_template('students/password.html',msg=msg)
#         return render_template('password.html')