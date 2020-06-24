from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import random

app = Flask(__name__)


@app.route('/')
def index():
    return "home"


# create employee route
@app.route('/employee/create')
def create_employee():
    return render_template('employee/create_employee.template.html')


# process create-employee form
@app.route('/employee/create', methods=['POST'])
def process_create_employee():
    print(request.form)
    with open('data.csv', 'a', newline="\n") as fp:  # a = append
        writer = csv.writer(fp, delimiter=",")
        id = random.randint(10000, 99999)
        name = request.form.get('employee-name')
        job_title = request.form.get('job-title')
        salary = request.form.get('salary')
        writer.writerow([id, name, job_title, salary])
    return "form received"


# read : for문을 이용해서 읽어들일꺼임
@app.route('/employees')
def read_employee():
    all_employees = []  # accumulator. State variable이라고도 함. 밑에 for문에서 'all_employees.appen({})' 라고 쓰고 이 dictionary를 통해서 여기다가 다 넣을꺼임
    # fp = open('data.csv', 'r', newline="\n")
    with open('data.csv', 'r', newline="\n") as fp:
        reader = csv.reader(fp, delimiter=",")
        next(reader)  # 요걸 넣음으로서 밑의 for문 돌릴 때,it skips the header
        for line in reader:
            all_employees.append({
                'id': line[0],
                'employee_name': line[1],
                'job_title': line[2],
                'salary': line[3]
            })
            print(line)
            print(all_employees)
    return render_template('employee/view_employees.template.html',
                           employees=all_employees
                           )
    # fp.close()


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)