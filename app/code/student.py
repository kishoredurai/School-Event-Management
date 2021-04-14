from app import  *

@app.route('/home', methods=["GET", "POST"])



def home():


    if 'username' in session:
        num = int(request.args['num'])
        username = session['username']
        pas=session['password']

        print(username)







        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE student_contact = %s', (username))
        # Fetch one record and return result
        account = cursor.fetchone()
        print(account)


        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s', (account['student_grade'],))
        subject = cursor.fetchall()
        print(subject)



        return render_template('students/home.html', res=account, subject=subject, len=len(subject),b=account['student_grade'],sweetalert=num)
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
        cursor.execute('Select * from course where course_grade=%s and subject_id=%s ', [b, a])
        course1 = cursor.fetchall()
        print(course1)
        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s', (b))
        subject = cursor.fetchall()
        session['loggedin'] = False
        return render_template('students/subcourse.html',course1=course1,subject=subject,len1=len(course1),len=len(subject),b=b)
    else:
        return redirect(url_for('login'))
        
        



@app.route("/sub_content", methods=["GET", "POST"])
def sub_content():
    if 'username' in session:


        c = request.args.get('c')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM course_chapter WHERE course_id  = %s', (c,))
        vid = cursor.fetchall()

        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s',(session['grade'],))
        subject = cursor.fetchall()

        return render_template('students/subject_content.html', vid=vid,len2=len(vid), subject=subject, len=len(subject),
                               b=session['grade'])
    else:
        return redirect(url_for('login'))

@app.route("/video", methods=["GET", "POST"])
def video():
    if 'username' in session:
        s=request.args.get('s')
        print(s)
        if s==None:
            n=0
        else:
            n=int(s)
            print(n)

        c = request.args.get('c')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM content_video,course_chapter_content where content_video.chapter_content_id = course_chapter_content.chapter_content_id and course_chapter_content.course_chapter_id =%s ', (c,))
        content = cursor.fetchall()
        print(content)



        cursor.execute('SELECT distinct subject.subject_name,course.subject_id FROM subject,course where course.subject_id=subject.subject_id and course.course_grade=%s',(session['grade'],))
        subject = cursor.fetchall()

        return render_template('students/video.html', content=content[n], len2=len(content), n=n, subject=subject, len=len(subject),
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