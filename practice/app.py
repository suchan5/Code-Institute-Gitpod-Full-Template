from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import random

app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome!'


@app.route('/create/members')
def create_members():
    return render_template('create.template.html')


@app.route('/create/members', methods=['POST'])
def process_members():
    print(request.form)
    with open('data.csv', 'a', newline="\n") as fp:
        writer = csv.writer(fp, delimiter=",")
        id = random.randint(10000, 99999)
        name = request.form.get('member-name')
        nickname = request.form.get('nickname')
        position = request.form.get('position')
        writer.writerow([id, name, nickname, position])
    return redirect(url_for('read_members'))


@app.route('/members')
def read_members():
    all_members = read_members_from_file()
    return render_template('read.template.html',
                           members=all_members
                           )


@app.route('/update/<member_id>')
def update_member(member_id):
    editing_member = find_member_by_id(member_id)
    return render_template('update.template.html',
                           member=editing_member)


def read_members_from_file():
    all_members = []
    with open('data.csv', 'r', newline="\n") as fp:
        reader = csv.reader(fp, delimiter=",")
        next(reader)
        for line in reader:
            all_members.append({
                'id': line[0],
                'member_name': line[1],
                'nickname': line[2],
                'position': line[3]
            })
    return all_members


def find_member_by_id(member_id):
    editing_member = None
    with open('data.csv', 'r', newline="\n") as fp:
        reader = csv.reader(fp, delimiter=",")
        next(reader)
        for line in reader:
            if member_id == line[0]:
                editing_member = {
                    'id': line[0],
                    'member_name': line[1],
                    'nickname': line[2],
                    'position': line[3]
                }
            break
    return editing_member


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)