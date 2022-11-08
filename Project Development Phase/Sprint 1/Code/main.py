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
    return render_template("signin.html")
@app.route("/signin/details",methods=["POST","GET"])
def details():
    if request.method == "POST":
        user_name = request.form['username']
        pass_word = request.form['password']
        query = "INSERT INTO users (user,pass) values (?,?)"
        insert_stmt = ibm_db.prepare(conn, query)
        ibm_db.bind_param(insert_stmt, 1, user_name)
        ibm_db.bind_param(insert_stmt, 2, pass_word)
        ibm_db.execute(insert_stmt)
        msg = 'Account Created Successfully'
        return render_template("details.html", msg=msg)
@app.route("/signin/details/stats",methods=["POST","GET"])
def final():
    if request.method == "POST":
        user_ = request.form['user']
        name_ = request.form['name']
        father_ = request.form['father']
        age_ = request.form['age']
        gender_ = request.form['gender']
        blood_ = request.form['blood']
        phone_ = request.form['phone']
        mail_ = request.form['mail']
        address_ = request.form['address']
        city_ = request.form['city']
        state_ = request.form['state']
        pin_ = request.form['pin']
        query1 = "INSERT INTO details (f_name,l_name,father,age,gender,blood,phone,mail,address,city,state,pin) values (?,?,?,?,?,?,?,?,?,?,?,?)"
        insert_stmt1 = ibm_db.prepare(conn, query1)
        ibm_db.bind_param(insert_stmt1, 1, user_)
        ibm_db.bind_param(insert_stmt1, 2, name_)
        ibm_db.bind_param(insert_stmt1, 3, father_)
        ibm_db.bind_param(insert_stmt1, 4, age_)
        ibm_db.bind_param(insert_stmt1, 5, gender_)
        ibm_db.bind_param(insert_stmt1, 6, blood_)
        ibm_db.bind_param(insert_stmt1, 7, phone_)
        ibm_db.bind_param(insert_stmt1, 8, mail_)
        ibm_db.bind_param(insert_stmt1, 9, address_)
        ibm_db.bind_param(insert_stmt1, 10, city_)
        ibm_db.bind_param(insert_stmt1, 11, state_)
        ibm_db.bind_param(insert_stmt1, 12, pin_)
        ibm_db.execute(insert_stmt1)
        print("success")
        return render_template("final.html")
if (__name__) == "__main__":
    app.run(debug=True)