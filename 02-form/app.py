from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)


# 반드시 'methods'라고 복수로 표기. 그리고 'GET'은 사실 default이기 때문에 안써도 된다
@app.route('/', methods=['GET'])
def home():
    return render_template('home.template.html')


@app.route('/', methods=['POST'])
def process_form():
    print(request.form)#마치 JS의 console.log처럼 이걸 함으로서 밑에 터미널 창에서 유저가 input한 값 확인 가능. 이건 항상 해주는게 습관이 되어야함
    username = request.form.get('username')#<input type="text" name="username"> 요기서 가져온다. 
    password = request.form.get('password')
    return render_template('process_form.template.html',
                           username=username,
                           password=password
                           )


@app.route('/bmi')
def calculate_bmi():
    return render_template('bmi.template.html')


@app.route('/bmi', methods=['POST'])
def process_bmi():
    print(request.form)
    weight = float(request.form.get('weight'))
    height = float(request.form.get('height'))
    bmi = weight / (height**2) * 10000
    return render_template('bmi-result.template.html',
                           weight=weight,
                           height=height,
                           bmi=bmi
                           )


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)