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
    #  return "form received" 요거 지우고 밑에처럼 url_for 써서 원하는 페이지로 이동하기 쉽게 바꿈 for better UI
    return redirect(url_for('read_employee'))


# read : for문을 이용해서 읽어들일꺼임 (얘도 열심히 작성했더니 refactoring때문에 다 지우네 ㅠㅠ )
@app.route('/employees')
def read_employee():
    all_employees = read_employees_from_file()
    return render_template('employee/view_employees.template.html',
                           employees=all_employees
                           )


# update : id를 중심으로 (기본적으로 위의 read랑 비슷. 사실 복붙해서 몇 개만 바꿔주면 된다. 근데 얘도 열심히 작성했더니 refactoring때문에 다 지우네ㅠㅠ)
@app.route('/employee/update/<employee_id>')
def update_employee(employee_id):
    editing_employee = find_employee_by_id(employee_id)
    return render_template('employee/update_employees.template.html',
                           employee=editing_employee
                           )


@app.route('/employee/update/<employee_id>', methods=['POST'])
def process_update_employee(employee_id):
    # Step 0. retrieve all the employees in the .csv file in a list
    all_employees = read_employees_from_file()

    # Step 1. find the employee that we have changed
    changed_employee = find_employee_by_id(employee_id)

    # Step 2. update the changed employee to match the form
    changed_employee['employee_name'] = request.form.get('employee-name')
    changed_employee['job_title'] = request.form.get('job-title')
    changed_employee['salary'] = request.form.get('salary')

    # Step 3. overwrite the employee information in the list
    for index in range(0, len(all_employees)):
        if all_employees[index]['id'] == changed_employee['id']:
            all_employees[index] = changed_employee

    # Step 4. write the entire list back to the csv file
    with open('data.csv', 'w', newline="\n") as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerow(['id', 'employee_name', 'job_title', 'salary'])  # 'employee_name'이라고 안하고 'name'이라고 했더니 에러뜸
        for e in all_employees:
            writer.writerow([e['id'], e['employee_name'], e['job_title'], e['salary']])  # 여기도 'employee_name'이라고 안하고 'name'이라고 했더니 에러뜸
    # return "Update finished" 요거 지우고 밑에처럼 url_for 써서 원하는 페이지로 이동하기 쉽게 바꿈 for better UI
    return redirect(url_for('read_employee'))


def read_employees_from_file():
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
    return all_employees
    # fp.close()


def find_employee_by_id(employee_id):
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
    return editing_employee


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)