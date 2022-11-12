from flask import Flask,render_template,request,redirect,url_for
import ibm_db
import os
app=Flask(__name__)

conn = ibm_db.connect(
    f"DATABASE={os.environ.get('DATABASE')};"
    f"HOSTNAME={os.environ.get('HOSTNAME')};"
    f"PORT={os.environ.get('PORT')};"
    f"USERNAME={os.environ.get('DB_USERNAME')};"
    f"PASSWORD={os.environ.get('PASSWORD')};"
    "SECURITY=SSL;"
    f"SSLSERVERCERTIFICATE={os.environ.get('SSLSERVERCERTIFICATE')};",
    '',
    ''
)

@app.route("/")
def front():
    return render_template("login.html")
@app.route("/login",methods=["POST","GET"])
def l_stats():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        # cursor = mysql.connection.cursor()
        # cursor.execute('SELECT * FROM register WHERE username = % s AND password = % s', (username, password ),)
        # account = cursor.fetchone()
        # print (account)

        sql = "SELECT * FROM Admin WHERE username = ? and password = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        result = ibm_db.execute(stmt)
        print(result)
        account = ibm_db.fetch_row(stmt)
        print(account)

        param = "SELECT * FROM Admin WHERE username = " + "\'" + username + "\'" + " and password = " + "\'" + password + "\'"
        res = ibm_db.exec_immediate(conn, param)
        dictionary = ibm_db.fetch_assoc(res)

        # sendmail("hello sakthi","sivasakthisairam@gmail.com")

        if account:
            session['loggedin'] = True
            # session['id'] = dictionary["ID"]
            # userid = dictionary["ID"]
            session['username'] = dictionary["USERNAME"]
            # session['email'] = dictionary["EMAIL"]

            return render_template('stats.html')
        else:
            msg = 'Incorrect username / password !'

    return render_template('login.html', msg=msg)

app.run()
