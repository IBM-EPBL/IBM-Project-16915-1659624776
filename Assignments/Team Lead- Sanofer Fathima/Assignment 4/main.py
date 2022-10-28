
from flask import Flask,render_template,request,redirect,url_for
app=Flask(__name__)

@app.route("/")
def home_page():
    return render_template("register.html")

if(__name__=='__main__'):
    app.run(host ='0.0.0.0', port = 5001)
