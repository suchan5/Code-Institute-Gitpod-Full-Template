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


# update : id를 중심으로 (기본적으로 위의 read랑 비슷 : 열심히 코딩 했는데 나중에 이 부분 다 지운다... for refactoring...)
@app.route('/employee/update/<employee_id>')
def update_employee(employee_id):
    editing_employee = None
    with open('data.csv', 'r', newline="\n") as fp:
        reader = csv.reader(fp, delimiter=",")
        next(reader)
        for line in reader:
            if line[0] == employee_id:
                editing_employee = {
                    'id': line[0],
                    'employee_name': line[1],
                    'job_title': line[2],
                    'salary': line[3]
                }
                break
    return render_template('employee/update_employees.template.html',
                           employee=editing_employee
                           )


@app.route('/employee/update/<employee_id>', methods=['POST'])
def process_update_employee(employee_id):
    # Step 0. retrieve all the employees in the .csv file in a list

    # Step 1. find the employee that we have changed

    # Step 2. overwrite the employee information in the list

    # Step 3. write the entire list back to the csv file
    pass