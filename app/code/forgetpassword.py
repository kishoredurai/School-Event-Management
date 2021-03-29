from app import *

@app.route("/verification", methods=["GET", "POST"])
def verification():
    if request.method == "POST":
        country_code = "+91"
        phone_number = request.form.get("phone_number")
        method = "sms"

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            'SELECT * FROM students WHERE mno= %s ', [phone_number])
        account = cursor.fetchone()

        cursor.execute(
            'SELECT * FROM teachers WHERE email= %s ', [phone_number])
        account1 = cursor.fetchone()

        if account:
            session['country_code'] = country_code
            session['phone_number'] = phone_number

            api.phones.verification_start(phone_number, country_code, via=method)
            return redirect(url_for("verify"))

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
            return Response("<h1>Failes!</h1>")

    return render_template("students/verification.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
            token = request.form.get("token")

            phone_number = session.get("phone_number")
            country_code = session.get("country_code")

            if phone_number=='':
                return render_template("changepwd.html")


            verification = api.phones.verification_check(phone_number,
                                                         country_code,
                                                         token)

            if verification.ok():
                return render_template("students/changepwd.html")
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
        cursor.execute('UPDATE teachers set pass=%s where email=%s',[passwd,email])
        mysql.connection.commit()
        return Response("<h1>Success!</h1>")
        #return Response("<h1>"+email+"</h1>")

    return render_template("students/emailpasswd.html")