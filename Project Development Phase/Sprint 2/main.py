from flask import *
from connect import *
import datetime
from urllib.parse import urlparse
from flask_mail import Mail,Message
import random
from followback import *
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
from connect import *
from flask import *
import datetime


def fetchapi(category):   # here images are fetched from respective buckets based on the category
    api=""
    if(category =='Women'):
        api='https://s3.jp-tok.cloud-object-storage.appdomain.cloud/raspberryibmsfrappbucket/'
    elif (category == 'Men'):
        api = 'https://s3.jp-tok.cloud-object-storage.appdomain.cloud/iraash/'
    elif (category == 'Accessories'):
        api = 'https://s3.jp-tok.cloud-object-storage.appdomain.cloud/104084smartfashion/'
    elif (category == 'Kids'):
        api = 'https://s3.jp-tok.cloud-object-storage.appdomain.cloud/iraash/'
    elif (category == 'Footwears'):
        api = 'https://s3.jp-tok.cloud-object-storage.appdomain.cloud/smartfashion2001/'
    return api

@app.route("/")
def home_page():
    logged_in_username = session.get('logged_in_username', None)
    logged_in_userid = session.get('logged_in_userid', None)
    return render_template("home.html",uname=logged_in_username,userid=logged_in_userid)

@app.route('/redirect_to')
def redirect_to():
    link = request.args.get('link', '/')
    return redirect(link), 301


def mail_service(mailid,sub,body):
    try:
        msg = Message(sub,sender="sashvogue@gmail.com",recipients=[mailid])
        msg.body = body
        mail.send(msg)
        print("Sent")
    except Exception as e:
        print("error")

@app.route("/register",methods=('GET','POST'))
def regpage():
    if request.method == 'POST':
        sub="Verify your email for Sash Vogue"
        form_checkvals = request.form.getlist("checkval")
        userid=str(random.randint(16565565445345,96565565445345))
        email = request.form['mail']
        dob=request.form['DOB']
        username = request.form['username']
        password=request.form['password']
        contact=request.form['contact']
        address=request.form['address']
        query="insert into user values('"+userid+"','"+username+"','"+contact+"','"+password+"','"+email+"','"+dob+"','"+address+"')"
        stmt=ibm_db.exec_immediate(conn,query)
        rowcount=ibm_db.num_rows(stmt) 
        body = "Hello "+username+", You have been registered successfully. Welcome to Sash Vogue Community."  #mail body
        if(len(form_checkvals) !=0  and form_checkvals[0]=='yes'):
            mail_service(email,sub,body)
        return redirect(url_for('loginpage'))
    return render_template("registration.html")

@app.route("/login",methods=('GET','POST'))
def loginpage():
    type='user'
    if request.method == 'POST':
        uname = request.form['uname']
        password = request.form['password']
        query = "select COUNT(*)from user where username='"+uname+"' and password='"+password+"'"
        stmt5 = ibm_db.exec_immediate(conn,query)
        row = ibm_db.fetch_tuple(stmt5)
        query1="select * from user where username='"+uname+"' and password='"+password+"'"
        stmt2= ibm_db.exec_immediate(conn,query1)
        row2= ibm_db.fetch_tuple(stmt2)
        if(row[0] ==1 ):
            session['logged_in_username'] = uname
            session['logged_in_userid'] = row2[0]
            print(row2[1])
            return redirect(url_for('home_page'))
        else:
            flash("Invalid credentials! Please enter correct details")
    return render_template("login.html",type=type)

  @app.route("/productdetails/<category>/<type>/<prodid>",methods=('GET','POST'))
def product_detailspg(category,type,prodid):
    o = urlparse(request.base_url) #to get the host naem of website url
    userid = session.get('logged_in_userid', None)
    uname = session.get('logged_in_username', None)
    if (request.method=='POST'):
        if(uname !=None):
            arr = fetch_cartarr(userid)
            insert_intocart(arr,prodid,category,userid,type)
        else:
            flash("Please login to add the products to cart")
    api=fetchapi(category)
    res18empty=False  #for some products we have only 4 images so to avaoid None error.
    res19empty=False
    query="select  o.*,p.pic1,p.pic2,p.pic3,p.pic1 from outfit o inner join picture p on o.prodid=p.prodid where o.prodid='"+prodid+"'"
    stmt = ibm_db.exec_immediate(conn, query)
    res = ibm_db.fetch_tuple(stmt)
    pricedisplay= round(res[2] -(res[2]*res[6] / 100))
    if ((res[18] == None) or (res[18] == "nil")):
        res18empty = True
    if( (res[19]==None) or (res[19]=="nil") ):
        res19empty=True
    return render_template("productdetails.html",category=category,type=type,prodid=prodid,result=res,api=api,res18empty=res18empty,res19empty=res19empty,pricedisplay=pricedisplay,hostname=o.hostname,port=o.port,uname=uname)

@app.route("/sunglasses_/<category>/<type>/<prodid>",methods=('GET','POST'))
def sunglasses_detailspg(category,type,prodid): # since sunglasses differ from other products in characteristics have to design separate page for this.
    o = urlparse(request.base_url)
    api=fetchapi(category)
    uname = session.get('logged_in_username', None)
    userid = session.get('logged_in_userid', None)
    if (request.method=='POST'):
        if (uname != None):
            arr = fetch_cartarr(userid)
            insert_intocart(arr, prodid, category, userid, type)
        else:
            flash("Please login to add the products to cart")   #if guest user tries to add to cart flash msg comes

    api=fetchapi(category)
    query="select  o.*,p.pic1,p.pic2,p.pic3,p.pic4,o.offer from sunglasses o inner join picture p on o.prodid=p.prodid where o.prodid='"+prodid+"'"
    stmt = ibm_db.exec_immediate(conn, query)
    res = ibm_db.fetch_tuple(stmt)
    pricedisplay = round(res[2] - (res[2] * res[17] / 100))
    return render_template("sunglasses_details.html",category=category,type=type,prodid=prodid,result=res,api=api,pricedisplay=pricedisplay,hostname=o.hostname,port=o.port,uname=uname)


@app.route("/products/<category>/<type>",methods=('GET','POST'))
def products_page(category,type):
    arr=[]
    userid = session.get('logged_in_userid', None)
    uname = session.get('logged_in_username', None)
    api=""
    if(request.method=='POST'):
        prodid=request.form['prodid']
        if(uname != None):
            insertwishlist="insert into wishlist values ('"+userid+"','"+prodid+"')"
            ibm_db.exec_immediate(conn,insertwishlist)
        else:
            flash("Please sign in to add products to the wishlist!")

    if(type != "Sunglasses"):

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
    return render_template("products.html",productsarr=arr,category=category,type=type,api=api,userid=userid,uname=uname)


if(__name__=='__main__'):
    app.run(host ='0.0.0.0', port = 5000)

