from connect import *
from flask import *
import datetime

#other use defined functions required
def fetchapi(category): 
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


def insert_intocart(arr,prodid,category,userid,type):
    dt=datetime.datetime.now()
    if (type == 'Dresses' or type == 'Kurtis' or type == 'Palazzo' or type == 'Western' or category == 'Men' or category == 'Kids' or category == 'Footwears'):
        size = request.form['sizeval']
    else:
        size = "nil"
    flag = 0

    for cartitems in arr:  #if already the user has added an item in cart quantity gets updated.
        if (cartitems[6] == prodid and cartitems[3]==size):
            flag = 1
            updatequery = "UPDATE cart set quantity=quantity+1 where prodid='" + prodid + "'"
            ibm_db.exec_immediate(conn, updatequery)
            break
    if (flag != 1):
        querycart="insert into cart values(?,?,?,?,?)"
        stmt = ibm_db.prepare(conn, querycart)
        ibm_db.bind_param(stmt, 1, userid)
        ibm_db.bind_param(stmt, 2, prodid)
        ibm_db.bind_param(stmt, 3, size)
        ibm_db.bind_param(stmt, 4, 1)
        ibm_db.bind_param(stmt, 5, dt)
        ibm_db.execute(stmt)

def fetch_cartarr(userid):
    arr=[]
    query = "select  o.prodname,o.price,p.pic1,c.size,o.category,o.type,o.prodid,o.offer,c.quantity from outfit o inner join picture p on o.prodid=p.prodid INNER join cart c on c.prodid=p.prodid where userid='"+userid+"' ORDER BY c.dateoadded DESC"
    stmt = ibm_db.exec_immediate(conn, query)
    row = ibm_db.fetch_tuple(stmt)
    while (row):
        arr.append(row)  # appending all dictionaries in arr
        row = ibm_db.fetch_tuple(stmt)  # incrementing that is to next row
    for i in range(0, len(arr)):
        arr[i] = list(arr[i])
    for j in range(0, len(arr)):
        imageapi = fetchapi(arr[j][4])
        arr[j][2] = imageapi + arr[j][2]
    constlen = len(arr)
    sunquery = "select o.prodname,o.price,p.pic1,c.size,o.category,o.type,o.prodid,o.offer,c.quantity from sunglasses o inner join picture p on o.prodid=p.prodid INNER join cart c on c.prodid=p.prodid where userid='"+userid+"' ORDER BY c.dateoadded DESC"
    sunstmt = ibm_db.exec_immediate(conn, sunquery)
    sunrow = ibm_db.fetch_tuple(sunstmt)
    while (sunrow):
        arr.append(sunrow)  # appending all dictionaries in arr
        sunrow = ibm_db.fetch_tuple(sunstmt)  # incrementing that is to next row
    for i in range(constlen, len(arr)):
        arr[i] = list(arr[i])
    for j in range(constlen, len(arr)):
        imageapi2 = fetchapi(arr[j][4])
        arr[j][2] = imageapi2 + arr[j][2]
    print(arr)
    return arr

def totamtcalculation(arr):
    totcost = 0
    totdis = 0
    amtarr=[]
    for k in range(0, len(arr)):
        totcost = totcost + (arr[k][1] * arr[k][8])
        temp = (arr[k][1] * arr[k][8] * arr[k][7]) / 100
        totdis = totdis + round(temp)
    netamt = totcost - totdis
    taxcalcnetamt = netamt + (netamt * 12) / 100
    amtarr.append(int(totcost))
    amtarr.append(int(totdis))
    amtarr.append(int(taxcalcnetamt))
    return amtarr

def fetchwishlist(userid):
    arr=[]
    query = "select  o.prodid,o.prodname,o.price,p.pic1,o.category,o.type,o.brand,o.offer from outfit o inner join picture p on o.prodid=p.prodid INNER join wishlist w on w.prodid=p.prodid where userid='" + userid + "'"
    stmt = ibm_db.exec_immediate(conn, query)
    row = ibm_db.fetch_tuple(stmt)
    while (row):
        arr.append(row)  # appending all dictionaries in arr
        row = ibm_db.fetch_tuple(stmt)  # incrementing that is to next row
    for i in range(0, len(arr)):
        arr[i] = list(arr[i])
    for j in range(0, len(arr)):
        imageapi = fetchapi(arr[j][4])
        arr[j][3] = imageapi + arr[j][3]
    constlen = len(arr)
    sunquery = "select o.prodid,o.prodname,o.price,p.pic1,o.category,o.type,o.brand,o.offer from sunglasses o inner join picture p on o.prodid=p.prodid INNER join wishlist w on w.prodid=p.prodid where userid='" + userid + "'"
    sunstmt = ibm_db.exec_immediate(conn, sunquery)
    sunrow = ibm_db.fetch_tuple(sunstmt)
    while (sunrow):
        arr.append(sunrow)  # appending all dictionaries in arr
        sunrow = ibm_db.fetch_tuple(sunstmt)  # incrementing that is to next row
    for i in range(constlen, len(arr)):
        arr[i] = list(arr[i])
    for j in range(constlen, len(arr)):
        imageapi2 = fetchapi(arr[j][4])
        arr[j][3] = imageapi2 + arr[j][3]
    return  arr
