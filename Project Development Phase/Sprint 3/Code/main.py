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
    return render_template("stats.html")
@app.route("/plasmadonate",methods=["POST","GET"])
def plasmadonate():
    if request.method == "POST":
        param1 = "SELECT * FROM details WHERE username = "+ "\'"+user + "\'"
        res1 = ibm_db.exec_immediate(conn, param1)
        dictionary1 = ibm_db.fetch_assoc(res1)
        donor_list=[]
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
app.run(debug=True)