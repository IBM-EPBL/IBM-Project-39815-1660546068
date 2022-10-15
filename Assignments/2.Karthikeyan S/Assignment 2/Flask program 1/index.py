# Flask program which should display name, Email, Phone and it should display the same details once we hit submit
from flask import Flask,render_template,request

app = Flask(__name__)
@app.route("/")
def front_page():
    return render_template("front_page.html")
@app.route("/final",methods=["POST","GET"])
def final_page():
    if request.method=="POST":
        datas=request.form
        return render_template("final_page.html",datas=datas)
if __name__=="__main__":
    app.run(debug=True)