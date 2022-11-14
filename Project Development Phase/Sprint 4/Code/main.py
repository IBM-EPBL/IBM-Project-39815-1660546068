from flask import Flask,render_template,request,session,redirect,url_for
import ibm_db
app=Flask(__name__)
app.secret_key='hidden'
conn=ibm_db.connect(
    f"DATABASE=bludb;"
    f"HOSTNAME=8e359033-a1c9-4643-82ef-8ac06f5107eb.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;"
    f"PORT=30120;"
    f"USERNAME=dws78237;"
    f"PASSWORD=OqY2YwnXTGpH4oGh;"
    "SECURITY=SSL;"
    f"SSLSERVERCERTIFICATE=DigiCertGlobalRootCA.crt;",
    '',
    ''
)
@app.route("/")
def front():
    return render_template("stats.html")
@app.route("/plasmarequest",methods=["POST","GET"])
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