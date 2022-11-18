from flask import *
from connect import *
import datetime
from urllib.parse import urlparse
import smtplib
import random
from followback import *
app= Flask(__name__)
app.config['SECRET_KEY'] = 'df0331cefc6c2b9a5d0208a726a5d1c0fd37324feba25506'
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login("fashionatsashvogue@gmail.com","nhmhbqmdeuxrhvwv")
#cart page
@app.route("/cart",methods=('GET','POST'))
def cart_page():
    userid=session.get('logged_in_userid', None)
    uname = session.get('logged_in_username', None)
    arr = fetch_cartarr(userid)

    amtarr=totamtcalculation(arr)
    if request.method == 'POST':
        prodid = request.form['prodid']
        print(prodid+"PRODID FROM CART")
        print(arr)
        flag = 0
        for cartitems in arr:
            if (cartitems[6] == prodid and cartitems[8] > 1):
                flag = 1
                updatequery = "UPDATE cart set quantity=quantity-1 where prodid='" + prodid + "'"
                ibm_db.exec_immediate(conn, updatequery)
        if (flag != 1):
            querycart = "DELETE from cart where prodid='" + prodid + "'"
            ibm_db.exec_immediate(conn, querycart)
    return  render_template("cart.html",cartarr=arr,totcost=amtarr[0],totdis=amtarr[1],netamt=amtarr[2],uname=uname,lencartarr=len(arr))
@app.route("/")
def home_page():
    logged_in_username = session.get('logged_in_username', None)
    logged_in_userid = session.get('logged_in_userid', None)
    return render_template("home.html",uname=logged_in_username,userid=logged_in_userid)

#logout page
@app.route("/logout")
def logout_pg():
    session.clear()
    return redirect(url_for('loginpage'))

@app.route('/redirect_to')
def redirect_to():
    link = request.args.get('link', '/')
    return redirect(link), 301
#registration page
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
        message = """Subject: Verify email for Sash Vogue

Hey """+username+""",\nYou have been successfully registered with Sash Vogue Community."""

        if(len(form_checkvals) !=0  and form_checkvals[0]=='yes'):
            server.sendmail("fashionatsashvogue@gmail.com",email,message)
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
            session['logged_in_usermail']=row2[4]
            print(row2[4])
            print(row2[1])
            return redirect(url_for('home_page'))
        else:
            flash("Invalid credentials! Please enter correct details")
    return render_template("login.html",type=type)



@app.route("/paymentredirect")
def payment_redirect():
    userid = session.get('logged_in_userid', None)
    umail=session.get('logged_in_usermail',None)
    arr=fetch_cartarr(userid)
    message = """Subject: Order Confirmation

Thank you for your order!. Your order has been received. Continue Shopping with Sash Vogue"""
    for item in arr:
        temp=item[1]-(item[1]*item[8]*item[7]/100)
        bill=int(temp)
        dt=datetime.datetime.now()
        query="insert into orders values(?,?,?,?,?)"
        stmt=ibm_db.prepare(conn,query)
        ibm_db.bind_param(stmt,1,userid)
        ibm_db.bind_param(stmt, 2,item[6])
        ibm_db.bind_param(stmt, 3,item[8])
        ibm_db.bind_param(stmt, 4, bill)
        ibm_db.bind_param(stmt, 5, dt)
        ibm_db.execute(stmt)
        server.sendmail("fashionatsashvogue@gmail.com", umail, message)

    return redirect(url_for('redirect_to',link='https://rzp.io/l/Ninl0NjQ'))
@app.route("/payment",methods=('GET','POST'))
def payment_pg():
    userid = session.get('logged_in_userid', None)
    uname = session.get('logged_in_username', None)
    arr = fetch_cartarr(userid)
    actualmon=datetime.date.today().month
    actualday=datetime.date.today().day
    amtarr = totamtcalculation(arr)
    print(amtarr)
    if request.method == 'POST':    #coupon generation if price >1000
        print("success")
        couponcode=request.form['couponcode']
        print(couponcode)
        address=request.form['address']
        print(amtarr)
        updateaddr="UPDATE user SET address='"+address+"' WHERE userid='"+userid+"'"
        ibm_db.exec_immediate(conn, updateaddr)
        if(len(arr)!=0):   #birthdaycoupon generation
            if (couponcode == 'shop25sv'):
                amtarr[2] = amtarr[2] - (amtarr[2] * 0.25)
            elif (couponcode == 'shi30obd'):
                amtarr[2] = amtarr[2] - (amtarr[2] * 0.3)
            elif (couponcode == 'sash50sma'):
                amtarr[2] = amtarr[2] - (amtarr[2] * 0.5)
            elif (couponcode == 'HBD60SAN'):
                amtarr[2] = amtarr[2] - (amtarr[2] * 0.6)
            print(amtarr)


    query="select DOB,address from user where userid='"+userid+"'"
    stmt = ibm_db.exec_immediate(conn, query)
    res = ibm_db.fetch_tuple(stmt)
    userdob=datetime.datetime.strptime(str(res[0]), "%Y-%m-%d")
    userdobmon=userdob.month
    userdobday=userdob.day

    if(userdobmon == actualmon and userdobday == actualday):
        birthdaycoupon=True
    else:
        birthdaycoupon=False

    return render_template("payment.html",netamt=amtarr[2],birthdaycoupon=birthdaycoupon,userid=userid,res=res,uname=uname)

@app.route("/addstock")
def add_Stockpg():
    return render_template("addstock.html")
@app.route("/adminlogin",methods=('GET','POST'))
def adminloginpage():
    type='admin'
    if request.method == 'POST':
        actualuname='admin'
        actualpassword='123'
        uname = request.form['uname']
        password = request.form['password']
        if(actualpassword == password and actualuname == uname ):
             return redirect(url_for('home_page'))
        else:
            flash("Invalid credentials! Please enter correct details")
    return render_template("login.html",type=type)



@app.route('/admin')
def adminhomepage():
    arr=[]
    query="select prodid,prodname,category,type,brand,price from outfit ORDER BY prodid"
    stmt = ibm_db.exec_immediate(conn, query)
    row = ibm_db.fetch_tuple(stmt)
    while (row):
        arr.append(row)  # appending all dictionaries in arr
        row = ibm_db.fetch_tuple(stmt)  # incrementing that is to next row

    return render_template("adminhome.html",prodarr=arr)

@app.route("/productdetails/<category>/<type>/<prodid>",methods=('GET','POST'))
def product_detailspg(category,type,prodid):
    o = urlparse(request.base_url)
    userid = session.get('logged_in_userid', None)
    uname = session.get('logged_in_username', None)
    if (request.method=='POST'):
        if(uname !=None):
            arr = fetch_cartarr(userid)
            insert_intocart(arr,prodid,category,userid,type)
            return redirect(url_for('cart_page'))
        else:
            flash("Oops! Seems like you haven't registered with us. Sign Up")
    api=fetchapi(category)
    res18empty=False
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
def sunglasses_detailspg(category,type,prodid):
    o = urlparse(request.base_url)
    api=fetchapi(category)
    uname = session.get('logged_in_username', None)
    userid = session.get('logged_in_userid', None)
    if (request.method=='POST'):
        if (uname != None):
            arr = fetch_cartarr(userid)
            insert_intocart(arr, prodid, category, userid, type)
        else:
            flash("Please login to add the products to cart")
    api=fetchapi(category)
    query="select  o.*,p.pic1,p.pic2,p.pic3,p.pic4,o.offer from sunglasses o inner join picture p on o.prodid=p.prodid where o.prodid='"+prodid+"'"
    stmt = ibm_db.exec_immediate(conn, query)
    res = ibm_db.fetch_tuple(stmt)
    pricedisplay = round(res[2] - (res[2] * res[17] / 100))
    return render_template("sunglasses_details.html",category=category,type=type,prodid=prodid,result=res,api=api,pricedisplay=pricedisplay,hostname=o.hostname,port=o.port,uname=uname)

@app.route('/wishlist')
def wishlist_pg():
    userid = session.get('logged_in_userid', None)
    uname = session.get('logged_in_username', None)
    arr=fetchwishlist(userid)
    return render_template("wishlist.html",wishlistarr=arr,uname=uname)

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
            flash("Oops! Seems like you haven't registered with us. Sign Up")

    if(type != "Sunglasses"): #since sunglasses differ some characteristics with other products need to create separate page.

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

