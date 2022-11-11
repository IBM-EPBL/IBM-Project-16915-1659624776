from flask import *
from connect import *
import datetime
from urllib.parse import urlparse
from flask_mail import Mail,Message
import random
app= Flask(__name__)
mail=Mail(app)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'
app.config['MAIL_SERVER']="smtp.gmail.com"
app.config['MAIL_PORT']=587
app.config['MAIL_USERNAME']='sashvogue@gmail.com'
app.config['MAIL_PASSWORD']="ptefzzenjtftzszl"
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=False
mail=Mail(app)

def mail_service(mailid,sub,body):
    try:
        msg = Message(sub,sender="sashvogue@gmail.com",recipients=[mailid])
        msg.body = body
        mail.send(msg)
        print("Sent")
    except Exception as e:
        print("error")
        
@app.route("/")
def home_page():
    logged_in_username = session.get('logged_in_username', None)
    logged_in_userid = session.get('logged_in_userid', None)
    return render_template("home.html",uname=logged_in_username,userid=logged_in_userid)

@app.route('/redirect_to')
def redirect_to():
    link = request.args.get('link', '/')
    return redirect(link), 301

@app.route("/register",methods=('GET','POST'))
def regpage():
    if request.method == 'POST':
        sub="Verify your email for Sash Vogue"
        form_checkvals = request.form.getlist("checkval")
        userid=str(random.randint(16565565445345,96565565445345))
        email = request.form['mail']
        username = request.form['username']
        password=request.form['password']
        contact=request.form['contact']
        doorno=request.form['doorno']
        streetflat=request.form['streetflat']
        area=request.form['area']
        landmark=request.form['landmark']
        city=request.form['city']
        state=request.form['state']
        country=request.form['country']
        pincode=request.form['pincode']
        query="insert into user values('"+userid+"','"+username+"','"+contact+"','"+password+"','"+email+"','"+doorno+"','"+streetflat+"','"+area+"','"+landmark+"','"+city+"','"+pincode+"','"+state+"','"+country+"')"
        stmt=ibm_db.exec_immediate(conn,query)
        rowcount=ibm_db.num_rows(stmt)
        body = "Hello "+username+", You have been registered successfully. Welcome to Sash Vogue Community."
        if(len(form_checkvals) !=0  and form_checkvals[0]=='yes'):
            mail_service(email,sub,body)
        return redirect(url_for('loginpage'))
    return render_template("registration.html")

@app.route("/login",methods=('GET','POST'))
def loginpage():
    if request.method == 'POST':
        uname = request.form['uname']
        password = request.form['password']
        query = "select COUNT(*)from user where username='"+uname+"' and password='"+password+"'"
        stmt5 = ibm_db.exec_immediate(conn,query)
        row = ibm_db.fetch_tuple(stmt5)
        query1="select * from user where username='"+uname+"' and password='"+password+"'"
        stmt2= ibm_db.exec_immediate(conn,query1)
        row2= ibm_db.fetch_tuple(stmt2)
        session['logged_in_username'] = uname
        session['logged_in_userid']=row2[0]
        if(row[0] ==1 ):
            print(row2[1])
            return redirect(url_for('home_page'))
        else:
            flash("Invalid credentials! Please enter correct details")
    return render_template("login.html")

def products_page(category,type):
    arr=[]
    api=""
    if(type != "Sunglasses"): #for sunglasses alone spearate page since prod attribute varies largely.
        api=fetchapi(category)
        query="select  o.prodid,o.prodname,o.brand,o.price,p.pic1,p.pic2,p.pic3,p.pic4,o.offer from outfit o inner join picture p on o.prodid=p.prodid where category='"+category+"' and type='"+type+"'"
        stmt = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_tuple(stmt)
        while (row):
            arr.append(row)  # appending all dictionaries in arr
            row = ibm_db.fetch_tuple(stmt)  # incrementing that is to next row
    else:
        api = fetchapi(category)
        query = "select  o.prodid,o.prodname,o.brand,o.price,p.pic1,p.pic2,p.pic3,p.pic4,o.offer from sunglasses o inner join picture p on o.prodid=p.prodid where category='"+category+"' and type='"+type+"'"
        stmt = ibm_db.exec_immediate(conn, query)
        row  = ibm_db.fetch_tuple(stmt)
        while (row):
            arr.append(row)  # appending all dictionaries in arr
            row = ibm_db.fetch_tuple(stmt)  # incrementing that is to next row
    return render_template("products.html",productsarr=arr,category=category,type=type,api=api)
  
 

if(__name__=='__main__'):
    app.run(host ='0.0.0.0', port = 5000)
