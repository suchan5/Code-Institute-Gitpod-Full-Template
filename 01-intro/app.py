from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hellow World"


@app.route('/about-us')
def about():
    return "About Me"


@app.route('/catalog')
def show_catalog():
    return render_template('catalog.template.html')


@app.route('/greetings/<name>')
def greet(name):
    return "Hello " + name


@app.route('/add/<n1>/<n2>')
def add(n1, n2):
    return str(int(n1) + int(n2))


@app.route('/add2/<int:n1>/<int:n2>')
def add_2(n1, n2):
    return str(n1 + n2)


@app.route('/add3/<N1>/<N2>')
def add_3(N1, N2):
    r = int(N1) + int(N2)
    return render_template('results.template.html', resultHoho=r)
    # 'r=resultHoho'이라고 쓰면 동작 안함-_-


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True) 