from app import *

@app.route("/verification", methods=["GET", "POST"])
def verification():
    if request.method == "POST":
        country_code = "+91"
        phone_number = request.form.get("phone_number")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE student_contact= %s ', [phone_number])
        account = cursor.fetchone()

        if account:
            session['country_code'] = country_code
            session['phone_number'] = phone_number

            api.phones.verification_start(phone_number, country_code, via='sms')
            return redirect(url_for("verify"))

        cursor.execute('SELECT * FROM teacher WHERE teacher_emailid= %s ', [phone_number])
        account1 = cursor.fetchone()

        if account1:

            session['country_code'] = country_code
            session['phone_number'] = phone_number

            msg = Message(
                'Hello',
                sender='ssig432@gmail.com',
                recipients=[phone_number]
            )

            msg.body = 'http://127.0.0.1:5000/passwdemail/' + phone_number
            mail.send(msg)

            return Response("<h1>Mail Sent Successfully!</h1>")

        else:
            flash("Invalid Username!")
            return redirect(url_for('verification'))

    return render_template("verification.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
            token = request.form.get("token")

            phone_number = session.get("phone_number")
            country_code = session.get("country_code")

            if phone_number=='':
                return render_template("changepwd.html")


            verification = api.phones.verification_check(phone_number,country_code,token)

            if verification.ok():
                return render_template("changepwd.html")
            else:
                flash("Invalid One Time Password !")
                return redirect(url_for('verify'))
                # return Response("<h1>Success!</h1>")

    return render_template("verify.html")

@app.route("/passwdemail/<name>")
def passwdemail(name):
        session['emailid'] = name
        return redirect(url_for("emailpasswd"))

@app.route("/emailpasswd", methods=["GET", "POST"])
def emailpasswd():
    email = session.get("emailid")
    if request.method == "POST":
        passwd = request.form.get("epasswd")
        email = session.get("emailid")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE teacher set teacher_password=%s where teacher_emailid=%s',[passwd,email])
        mysql.connection.commit()
        return Response("<h1>Success!</h1>")
        #return Response("<h1>"+email+"</h1>")

    return render_template("students/emailpasswd.html")

@app.route("/changepwd", methods=["GET", "POST"])
def changepwd():
        if request.method == "POST":
            passwd = request.form.get("passwd")
            phone_number = session.get("phone_number")
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE student set student_password=%s where student_contact=%s', [passwd,phone_number])
            mysql.connection.commit()
            flash("Done !")
            return redirect(url_for('changepwd'))
        return render_template("changepass.html")