from flask import Flask, render_template, request, redirect, url_for
import os
import csv
import random

app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome!'


@app.route('/member/create')
def create_members():
    return render_template('member/create.template.html')


@app.route('/member/create', methods=['POST'])
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


@app.route('/member/members')
def read_members():
    all_members = read_members_from_file()
    return render_template('member/read.template.html',
                           members=all_members
                           )


@app.route('/member/update/<member_id>')
def update_member(member_id):
    editing_member = find_member_by_id(member_id)
    return render_template('member/update.template.html',
                           member=editing_member)


@app.route('/member/update/<member_id>', methods=['POST'])
def process_update_member(member_id):
    all_members = read_members_from_file()
    changed_member = find_member_by_id(member_id)
    changed_member['member_name'] = request.form.get('member-name')
    changed_member['nickname'] = request.form.get('nickname')
    changed_member['position'] = request.form.get('position')
    for index in range(0, len(all_members)):
        if all_members[index]['id'] == changed_member['id']:
            all_members[index] = changed_member
    with open('data.csv', 'w', newline="\n") as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerow(['id', 'member_name', 'nickname', 'position'])
        for m in all_members:
            writer.writerow([m['id'], m['member_name'], m['nickname'], m['position']])
    return redirect(url_for('read_members'))


@app.route('/member/confirm_delete/<member_id>')
def confirm_to_delete_member(member_id):
    member = find_member_by_id(member_id)
    return render_template('member/confirm_delete.template.html',
                           member=member
                           )


@app.route('/member/delete/<member_id>', methods=['POST'])
def delete_member(member_id):
    all_members = read_members_from_file()
    member_to_be_deleted = find_member_by_id(member_id)
    for index in range(len(all_members)):
        if member_to_be_deleted['id'] == all_members[index]['id']:
            del all_members[index]
            break

    write_to_file(all_members)
    return redirect(url_for('read_members'))


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


def write_to_file(all_members):
    with open('data.csv', 'w', newline="\n") as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerow(['id', 'member_name', 'nickname', 'position'])
        for m in all_members:
            writer.writerow([m['id'], m['member_name'], m['nickname'], m['position']])


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)