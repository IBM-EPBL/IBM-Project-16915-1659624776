from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def first_page():
    return render_template('home.html')


if(__name__ == '__main__'):
    app.run(host='0.0.0.0', port = 5001)