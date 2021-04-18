from app import  *





################## HOME PAGE ############


@app.route('/home', methods=["GET", "POST"])
def home():
    if 'username' in session and session.get("user_type") == 'student':
        stu_id=session.get('id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE student_id = %s',[stu_id])
        account = cursor.fetchone()
        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s',[account['student_grade']])
        subject = cursor.fetchall()
        return render_template('students/student_home.html', res=account, subject=subject, len=len(subject))
    else:
        return redirect(url_for('login'))

###################### PROFILE SECTION ################


@app.route("/profile", methods=["GET", "POST"])
def student_profile():
    if 'username' in session and session.get("user_type") == 'student' :
        stu_id=session.get('id')
        username = session['username']
        grade=session['grade']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE student_id  = %s', [stu_id])
        account = cursor.fetchone()
        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s',[grade])
        subject = cursor.fetchall()

        return render_template('students/student_profile.html', res=account, subject=subject, len=len(subject))
    else:
        return redirect(url_for('login'))



@app.route("/profile/update", methods=["GET", "POST"])
def profile_update():

    if 'username' in session and session.get("user_type") == 'student' and request.method == 'POST':       

        stu_id=session.get('id')
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
        cursor.execute('update student set student_Fname= %s, student_Lname=%s , student_school=%s, student_dob=%s , student_address=%s, student_add_district=%s,student_add_state=%s where student_id=%s', (fname,lname,sname,dob,add,city,state,stu_id))
        mysql.connection.commit()
        flash("profile data updated Successfully!")
        return redirect(url_for('student_profile'))

    else:
        return redirect(url_for('login'))

@app.route('/change_profile_image', methods = ['POST'])
def change_profile_image():
    if 'username' in session and session.get("user_type") == 'student' and request.method == 'POST':

        stu_id=session.get('id')
        f = request.files['file']
        filename = secure_filename(f.filename)
        path="static/img/profile_image/{0}".format(filename)
        f.save(os.path.join(app.root_path, path))
        path1="img/profile_image/{0}".format(filename)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('update student set student_profile_image=%s WHERE student_id  = %s', (path1,stu_id))
        mysql.connection.commit()
        flash("Profile Image Updated Successfully!")
        return redirect(url_for('student_profile'))
        
    else:
        return redirect(url_for('login'))


############# COURSE SECTION ###############################

@app.route("/courses")
def student_courses():
    if 'username' in session and session.get("user_type") == 'student':
        stu_id=session.get('id')
        grade=session.get('grade')

        a = request.args.get('sub_id')
        subname = request.args.get('sub_name')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('Select * from course where course_grade=%s and subject_id=%s ', [grade, a])
        course1 = cursor.fetchall()
        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s', [grade])
        subject = cursor.fetchall()
        cursor.execute('SELECT * FROM student WHERE student_id  = %s', [stu_id])
        account = cursor.fetchone()

        return render_template('students/student_course.html',course1=course1,res=account,subject=subject,len1=len(course1),len=len(subject),sub_name=subname)
    else:
        return redirect(url_for('login'))
        
        



@app.route("/course/chapter", methods=["GET", "POST"])
def student_course_chapter():
    if 'username' in session and session.get("user_type") == 'student':
        username = session['username']
        stu_id=session.get('id')
        c = request.args.get('courseid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE student_id  = %s', [stu_id])
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM course_chapter WHERE course_id  = %s', [c])
        vid = cursor.fetchall()

        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s',(session['grade'],))
        subject = cursor.fetchall()

        return render_template('students/course_chapter.html',res=account, vid=vid,len2=len(vid), subject=subject, len=len(subject))
    else:
        return redirect(url_for('login'))



################# COURSE ENROLL ##########################

@app.route('/course_enroll', methods=["POST", "GET"])
def course_enroll():
    test=0
    if 'username' in session and session.get("user_type") == 'student':
        stu_id=session.get('id')

        
        if request.method == "POST":
            
            if request.form.get("enroll"):

                result = request.form  # Get the data
                course = result["enroll"]
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('insert into course_enrollment(student_id, course_id, enroll_status) values(%s,%s,"Registered")', [stu_id,course])
                mysql.connection.commit()
                flash("Course Enrolled Successfully!")
                return redirect(url_for('course_enroll',courseid=course)) 


        course_id = request.args.get('courseid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('Select * from course where course_id = %s', [course_id])
        cc = cursor.fetchone()
        cursor.execute('Select * from course_enrollment where  course_id = %s', [course_id])
        courseenrol = cursor.fetchall()
        cursor.execute('SELECT * FROM student WHERE student_id = %s',[stu_id])
        account = cursor.fetchone()
        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s',[account['student_grade']])
        subject = cursor.fetchall()
        if(courseenrol):
            test=1
        
        return render_template('students/course_enroll.html',data=cc,test=test,res=account, subject=subject, len=len(subject))

















@app.route("/video", methods=["GET", "POST"])
def video():
    if 'username' in session and session.get("user_type") == 'student' :
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