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
        enroll_id=request.args.get('enroll_id')
        print(enroll_id)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE student_id  = %s', [stu_id])
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM course_chapter WHERE course_id  = %s', [c])
        vid = cursor.fetchall()
        cursor.execute('SELECT progress_percentage FROM course_enroll_progress WHERE enroll_id  = %s', (enroll_id,))
        percentage = cursor.fetchall()



        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s',(session['grade'],))
        subject = cursor.fetchall()

        return render_template('students/course_chapter.html',res=account, vid=vid,len2=len(vid), subject=subject, len=len(subject),percentage=percentage,enroll_id=enroll_id)
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
                last_id=cursor.lastrowid

                print(last_id)

                client.messages.create(to="+919787688154",from_="+15623795133",body="Hello from Python!")

                # cursor.execute('insert into course_enroll_progress(course_chapter_id,enroll_id) select(course_chapter_id,"%s") from course_chapter where course_id=%s', [last_id,course])
                # mysql.connection.commit()
                #cursor.execute('insert into ')

                flash("Course Enrolled Successfully!")
                return redirect(url_for('course_enroll',courseid=course)) 


        course_id = request.args.get('courseid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('Select * from course where course_id = %s', [course_id])
        cc = cursor.fetchone()
        cursor.execute('select * from course_chapter where course_id=%s',[course_id])
        details=cursor.fetchall()


        cursor.execute('Select * from course_enrollment where  course_id = %s and student_id=%s', [course_id,stu_id])
        courseenrol = cursor.fetchone()

        cursor.execute('SELECT * FROM student WHERE student_id = %s',[stu_id])
        account = cursor.fetchone()
        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s',[account['student_grade']])
        subject = cursor.fetchall()
        if(courseenrol):
            test=1
        
        return render_template('students/course_enroll.html',data=cc,test=test,res=account,details=details,len2=len(details), subject=subject, courseenrol=courseenrol,len=len(subject))



############################    MY COURSE     ############################

@app.route('/my_course', methods=["POST", "GET"])
def my_course():
    if 'username' in session and session.get("user_type") == 'student':
        stu_id = session.get('id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from course_enrollment,course where course.course_id=course_enrollment.course_id and course_enrollment.student_id=%s",([stu_id]))
        my_course = cursor.fetchall()
        cursor.execute(
            'SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s',
            (session['grade'],))
        subject = cursor.fetchall()
        cursor.execute('SELECT * FROM student WHERE student_id = %s', [stu_id])
        account = cursor.fetchone()

        return render_template('students/my_course.html',res=account,my_course=my_course,len1=len(my_course),len=len(subject),subject=subject)

















@app.route("/video", methods=["GET", "POST"])
def video():
    if 'username' in session and session.get("user_type") == 'student' :
        username = session['username']
        enroll_id=request.args.get('enroll_id')
        #s=request.args.get('s')

        #pro = request.args.get('pro')
        #print(pro)
        # c stands for course chapter id

        c = request.args.get('c')
        print(c)













        #if s==None:
        #    n=0
        #else:
         #   n=int(s)



        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE student_contact  = %s', (username,))
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM content_video,course_chapter_content where content_video.chapter_content_id = course_chapter_content.chapter_content_id and course_chapter_content.course_chapter_id =%s ', (c,))
        content = cursor.fetchall()

        cursor.execute('SELECT progress_percentage FROM course_enroll_progress WHERE course_chapter_id= %s and enroll_id=%s ', (c,enroll_id))
        percentage = cursor.fetchone()



        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s',(session['grade'],))
        subject = cursor.fetchall()

        return render_template('students/video.html', content=content,res=account, len2=len(content), subject=subject, len=len(subject),percentage=percentage,enroll_id=enroll_id ,c=c,b=session['grade'])
    else:
        return redirect(url_for('login'))
        
        


@app.route("/video_update/", methods=["POST","GET"])
def video_update():

    if request.method == "GET":
        print("hi")

        percentage = request.args.get('percentage')
        enroll_id=request.args.get('enroll_id')
        ch_id=request.args.get('ch_id')

        print(ch_id)
        print(enroll_id)
        print(percentage)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('update course_enroll_progress set progress_percentage = %s where enroll_id =%s and course_chapter_id=%s', (percentage,enroll_id,ch_id))
        mysql.connection.commit()

        return render_template('students/video.html')

















#msg=''
         #if request.method == "POST":
            #passwd = request.form.get("confirm_password")

            # phone_number = session.get("username")
             #print(phone_number)
            #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
             #cursor.execute('UPDATE students set pass=%s where mno=%s', [passwd,phone_number])
             #mysql.connection.commit()
             #msg="Password changed successfully !!!"
             #return render_template('students/password.html',msg=msg)