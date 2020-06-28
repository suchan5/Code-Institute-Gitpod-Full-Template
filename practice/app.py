from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import random

app = Flask(__name__)


# create employee
@app.route('/create')
def create_employee():
    return render_template('create.template.html')


@app.route('/create', methods=['POST'])
def process_create_employee():
    print(request.form)
    with open('data.csv', 'a', newline="\n") as fp:
        writer = csv.writer(fp, delimiter=",")
        id = random.randint(10000, 99999)
        member_name = request.form.get('member-name')
        nickname = request.form.get('nickname')
        position = request.form.get('position')
        writer.writerow([id, member_name, nickname, position])
    return redirect(url_for('read_employee'))


# read  employees
@app.route('/employees')
def read_employee():
    all_emplyoees = read_employees_from_file()
    return render_template('read_employee.template.html',
                           employees=all_emplyoees
                           )


def read_employees_from_file():
    all_employees = []
    with open('data.csv', 'r', newline="\n") as fp:
        reader = csv.reader(fp, delimiter=",")
        next(reader)
        for line in reader:
            all_employees.append({
                'id': line[0],
                'member_name': line[1],
                'nickname': line[2],
                'position': line[3]
            })
    return all_employees


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)