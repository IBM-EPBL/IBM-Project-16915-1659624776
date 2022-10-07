from flask import Flask,render_template
from objstorage import *
app= Flask(__name__)

@app.route("/chatbot")
def chat():
    return render_template("chatbot.html")


if(__name__=='__main__'):
    app.run()
