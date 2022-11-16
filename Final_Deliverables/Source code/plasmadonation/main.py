from flask import Flask,render_template,request,session,redirect,url_for
import ibm_db
import os
app=Flask(__name__)
app.secret_key='hidden'
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
print(conn)
@app.route("/")
def front():
    return render_template("front.html")
@app.route("/login",methods=["POST","GET"])
def login():
    return render_template("login.html")
@app.route("/signin",methods=["POST","GET"])
def signin():
    return render_template("signin.html")
@app.route("/signin/details/stats",methods=["POST","GET"])
def s_stats():
    if request.method == "POST":
        global user
        user=""
        user_=request.form['user']
        name_ = request.form['name']
        father_ = request.form['father']
        age_ = request.form['age']
        gender_=request.form['gender']
        blood_=request.form['blood']
        phone_ = request.form['phone']
        mail_ = request.form['mail']
        address_ = request.form['address']
        city_ = request.form['city']
        state_ = request.form['state']
        pin_ = request.form['pin']
        query1 = "INSERT INTO details (username,name,father,age,gender,blood,phone,mail,address,city,state,pin) values (?,?,?,?,?,?,?,?,?,?,?,?)"
        insert_stmt1 = ibm_db.prepare(conn, query1)
        ibm_db.bind_param(insert_stmt1, 1, user_)
        ibm_db.bind_param(insert_stmt1, 2,name_)
        ibm_db.bind_param(insert_stmt1, 3,father_)
        ibm_db.bind_param(insert_stmt1, 4,age_)
        ibm_db.bind_param(insert_stmt1, 5,gender_)
        ibm_db.bind_param(insert_stmt1, 6,blood_)
        ibm_db.bind_param(insert_stmt1, 7,phone_)
        ibm_db.bind_param(insert_stmt1, 8,mail_)
        ibm_db.bind_param(insert_stmt1, 9,address_)
        ibm_db.bind_param(insert_stmt1, 10,city_)
        ibm_db.bind_param(insert_stmt1, 11,state_)
        ibm_db.bind_param(insert_stmt1, 12,pin_)
        ibm_db.execute(insert_stmt1)
        print("success")
        user=user+user_
        return render_template("stats.html")
@app.route("/login/stats",methods=["POST","GET"])
def l_stats():
    if request.method == "POST":
        global user
        user=""
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
        print(param)
        res = ibm_db.exec_immediate(conn, param)
        print(res)
        dictionary = ibm_db.fetch_assoc(res)
        print(dictionary)
        # sendmail("hello sakthi","sivasakthisairam@gmail.com")
        msg=""
        if account:
            session['loggedin'] = True
            # session['id'] = dictionary["ID"]
            # userid = dictionary["ID"]
            session['username'] = dictionary["USERNAME"]
            # session['email'] = dictionary["EMAIL"]
            user=user+username
            return render_template('stats.html')
        else:
            msg = msg+'Incorrect username / password ! Try again'

    return render_template('login.html',message=msg)


@app.route("/signin/details",methods=["POST","GET"])
def details():
    if request.method == "POST":
        user_name=request.form['username']
        pass_word=request.form['password']
        c_pass_word = request.form['confirm_password']
        if pass_word==c_pass_word:
            query="INSERT INTO Admin (username,password) values (?,?)"
            insert_stmt = ibm_db.prepare(conn, query)
            ibm_db.bind_param(insert_stmt, 1, user_name)
            ibm_db.bind_param(insert_stmt, 2, pass_word)
            ibm_db.execute(insert_stmt)
            msg='Account Created Successfully'
            return render_template("details.html",msg=msg)
        else:
            return render_template("signin.html",message="Check the password")
@app.route("/login_success/stats",methods=["POST","GET"])
def lo_stats():
        return render_template("stats.html")
@app.route("/login/stats/plasmarequest",methods=["POST","GET"])
def plasmareq():
    if request.method == "POST":
        param = "SELECT * FROM donors"
        result = []
        print(param)
        res = ibm_db.exec_immediate(conn, param)
        print(res)
        dictionary = ibm_db.fetch_assoc(res)
        print(dictionary)
        while dictionary != False:
            result.append(dictionary)
            dictionary = ibm_db.fetch_assoc(res)
        data_=(tuple(result))
        print(data_)
        return render_template("plasmarequest.html", datas=data_)
@app.route("/login/stats/plasmadonate",methods=["POST","GET"])
def plasmadonate():
    if request.method == "POST":
        para = "SELECT * FROM donors WHERE username = " + "\'" + user + "\'"
        re = ibm_db.exec_immediate(conn, para)
        dict = ibm_db.fetch_assoc(re)
        print(re)
        print(dict)
        if(dict==False):
            param1 = "SELECT * FROM details WHERE username = " + "\'" + user + "\'"
            res1 = ibm_db.exec_immediate(conn, param1)
            dictionary1 = ibm_db.fetch_assoc(res1)
            donor_list = []
            for i in dictionary1.values():
                donor_list.append(i)
            query2 = "INSERT INTO donors (username,name,father,age,gender,blood,phone,mail,address,city,state,pin) values (?,?,?,?,?,?,?,?,?,?,?,?)"
            insert_stmt2 = ibm_db.prepare(conn, query2)
            ibm_db.bind_param(insert_stmt2, 1, donor_list[0])
            ibm_db.bind_param(insert_stmt2, 2, donor_list[1])
            ibm_db.bind_param(insert_stmt2, 3, donor_list[2])
            ibm_db.bind_param(insert_stmt2, 4, donor_list[3])
            ibm_db.bind_param(insert_stmt2, 5, donor_list[4])
            ibm_db.bind_param(insert_stmt2, 6, donor_list[5])
            ibm_db.bind_param(insert_stmt2, 7, donor_list[6])
            ibm_db.bind_param(insert_stmt2, 8, donor_list[7])
            ibm_db.bind_param(insert_stmt2, 9, donor_list[8])
            ibm_db.bind_param(insert_stmt2, 10, donor_list[9])
            ibm_db.bind_param(insert_stmt2, 11, donor_list[10])
            ibm_db.bind_param(insert_stmt2, 12, donor_list[11])
            ibm_db.execute(insert_stmt2)
            return render_template("plasmadonation.html")
        else:
            return render_template("plasmadonation.html")
if (__name__) == "__main__":
    app.run(debug=True)
