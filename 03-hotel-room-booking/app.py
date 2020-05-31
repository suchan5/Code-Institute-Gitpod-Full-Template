from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('show-form.template.html')


@app.route('/', methods=['POST'])
def process_form():
    print(request.form)
    firstname = request.form.get('first-name')
    lastname = request.form.get('last-name')
    comments = request.form.get('comments')
    roomtype = request.form.get('room-type')
    # for checkbox, we need to use 'request.form.getlist'
    amenities = request.form.getlist('amenities')
    checkintime = request.form.get('check-in-timing')
    return render_template('results.template.html',
                           firstname=firstname,
                           lastname=lastname,
                           comments=comments,
                           roomtype=roomtype,
                           amenities=", ".join(amenities), # 요렇게 안하면 결과값이 list로 나옴
                           checkintime=checkintime
                           )


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)