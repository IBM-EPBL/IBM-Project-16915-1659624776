from flask import Flask,render_template,request,redirect,url_for
from connect import *
app=Flask(__name__)
@app.route('/')
def home_page():
    return render_template("home.html")
@app.route("/register",methods=('GET','POST'))
def regpage():
    if request.method == 'POST':
        rollno = request.form['rollno']
        uname = request.form['uname']
        mail=request.form['mail']
        password=request.form['password']
        query="insert into user values('"+rollno+"','"+mail+"','"+password+"','"+uname+"')"
        stmt=ibm_db.exec_immediate(conn,query)
        rowcount=ibm_db.num_rows(stmt)
        print(rowcount)
        return redirect(url_for('loginpage'))
    return render_template("registration.html")
@app.route("/",methods=('GET','POST'))
@app.route("/login",methods=('GET','POST'))
def loginpage():
    if request.method == 'POST':
        uname = request.form['uname']
        password = request.form['password']
        query = "select COUNT(*) from user where username='"+uname+"' and password='"+password+"'"
        stmt5 = ibm_db.exec_immediate(conn,query)
        row = ibm_db.fetch_tuple(stmt5)
        if(row[0] ==1 ):
            return render_template("home.html")
    return render_template("login.html")
@app.route("/assign3")

@app.route('/redirect_to')
def redirect_to():
    link = request.args.get('link', '/')
    return redirect(link), 301
@app.route("/chatbot")
def chat():
    return render_template("chatbot.html")
if(__name__=='__main__'):
    app.run()