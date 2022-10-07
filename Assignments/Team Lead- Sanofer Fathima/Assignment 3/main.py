from flask import Flask,render_template
from objstorage import *
app= Flask(__name__)

@app.route("/chatbot")
def chat():
    return render_template("chatbot.html")

@app.route("/assign3")
def objstorage():
 for i in range(0,len(imagearr)):
 imagearr[i]="https://s3.jp-tok.cloud-objectstorage.appdomain.cloud/sanrasheed29/"+imagearr[i]
 print("objstorage ", imagearr)
 return render_template('assign3.html',arr=imagearr)

@app.route('/redirect_to')
def redirect_to():
 link = request.args.get('link', '/')
 return redirect(link), 301

if(__name__=='__main__'):
    app.run()
