from flask import Flask, render_template, redirect, url_for, jsonify, request
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv
from sqlmodel import create_engine
from flask_wtf import CSRFProtect
from models import *
from datetime import datetime
import datetime
import os

load_dotenv('.env')
app = Flask(__name__)
app.config['SECRET_KEY'] =  os.environ.get('SECRET_KEY')
csrf = CSRFProtect(app)
db_engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))


accounts = [
    {
        'account_id' : '789678464354623',
        'name' : 'Edison Electric',
        'email' : 'me@ex.net',
        'password' : 'test_123344',
        'date_added' : datetime.datetime.now(),
        'mobile' : '909551234',
        'category' : 'Utilities',
        'due_date' : datetime.date(2025, 10, 26),
        'amount' : 120,
        'note' : 'You have a 5 day grace period'
    },
    {
        'account_id' : '67845653542w5642',
        'name' : 'Wells Fargo',
        'email' : 'me@ex.net',
        'password' : 'test_123344',
        'date_added' : datetime.date(2025, 9, 12),
        'mobile' : '909551234',
        'category' : 'Banking',
        'due_date' : datetime.date(2025, 8, 29),
        'amount' : None,
        'note' : 'You have a 5 day grace period'
    },
    {
        'account_id' : '46326534245324500',
        'name' : 'Netflix',
        'email' : 'me@ex.net',
        'password' : 'test_123344',
        'date_added' : datetime.date(2025, 8, 26),
        'mobile' : '909551234',
        'category' : 'Entertainment',
        'due_date' : datetime.date(2025, 10, 10),
        'amount' : 12.99,
        'note' : 'You have a 5 day grace period'
    },
    {
        'account_id' : '8686456734645353425',
        'name' : 'Hulu',
        'email' : 'me@ex.net',
        'password' : 'test_123344',
        'date_added' : datetime.date(2025, 9, 12),
        'mobile' : '909551234',
        'category' : 'Entertainment',
        'due_date' : datetime.date(2025, 11, 2),
        'amount' : 18.99,
        'note' : 'You have a 5 day grace period'
    }
]



@app.route('/', methods=['GET','POST'])
@app.route('/register', methods=['GET','POST'])
@app.route('/register/', methods=['GET','POST'])
def homepage():
    return render_template('index.html')

@app.route('/signin', methods=['GET','POST'])
@app.route('/signin/', methods=['GET','POST'])
def signin():
    return render_template('signin.html')

@app.route('/forgot-password')
@app.route('/forgot-password/')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/check-email')
def check_email():
    return render_template('check_email.html')

@app.route('/send-link')
def send_link():
    #route to email link to user
    pass

@app.route('/change-password')
def change_password():
    return render_template('change_password.html')

@app.route('/password-reset')
def password_reset():
    return render_template('password_reset.html')

@app.route('/signout')
def signout():
    pass

@app.route('/password-generator', methods=['GET', 'POST'])
@app.route('/password-generator/', methods=['GET', 'POST'])
def password_gen():
   if request.method == 'POST':
     characters = request.form.get('character-type').upper()
     generated_password = Utilities.password_generator(
         request.form.get('password-length'),
         CharacterOptions[f"{characters}"]
     )
     return jsonify({'password' : generated_password})
   return render_template('password_generator.html', character_types=CharacterOptions)


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    notes = [
        {
            'note_id' : 1,
            'user_id' : 3,
            'title' : 'Walk the dog',
            'note' : 'Walk the dog in the morning, around lunch and twice in the evening',
            'category' : 'Chores',
            'date_added' : datetime.date(2025, 2, 12)
        },
        {
            'note_id' : 2,
            'user_id' : 3,
            'title' : 'Practice Thai',
            'note' : 'One hour in the morning daily',
            'category' : 'Study',
            'date_added' : datetime.date(2025, 3, 14)
        },
        {
            'note_id' : 3,
            'user_id' : 3,
            'title' : 'Call mom',
            'note' : 'Be sure you call her at least once a week',
            'category' : 'Appointment',
            'date_added' : datetime.date(2025, 6, 24)
        },
        {
            'note_id' : 4,
            'user_id' : 1,
            'title' : 'Schedule Dr Appt',
            'note' : 'Call Dr Mason and schedule an appt next week',
            'category' : 'Appointment',
            'date_added' : datetime.date(2025, 4, 10)
        }
    ]
    return render_template('notes.html')

@app.route('/note/view/<note_id>')
def view_note(note_id):
    pass

@app.route('/note/edit/<note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    notes = [
        {
            'note_id' : 1,
            'user_id' : 3,
            'title' : 'Walk the dog',
            'note' : 'Walk the dog in the morning, around lunch and twice in the evening',
            'category' : 'Chores',
            'date_added' : datetime.date(2025, 2, 12)
        },
        {
            'note_id' : 2,
            'user_id' : 3,
            'title' : 'Practice Thai',
            'note' : 'One hour in the morning daily',
            'category' : 'Study',
            'date_added' : datetime.date(2025, 3, 14)
        },
        {
            'note_id' : 3,
            'user_id' : 3,
            'title' : 'Call mom',
            'note' : 'Be sure you call her at least once a week',
            'category' : 'Appointment',
            'date_added' : datetime.date(2025, 6, 24)
        },
        {
            'note_id' : 4,
            'user_id' : 1,
            'title' : 'Schedule Dr Appt',
            'note' : 'Call Dr Mason and schedule an appt next week',
            'category' : 'Appointment',
            'date_added' : datetime.date(2025, 4, 10)
        }
    ]
    note = [note for note in notes if str(note['note_id']) == note_id]
    return jsonify({'note' : note})


@app.route('/note/remove/<note_id>', methods=['DELETE'])
def remove_note(note_id):
   pass

@app.route('/account-manager', methods=['GET', 'POST'])
def account_manager():
    return render_template('accounts.html', accounts=accounts)

@app.route('/account-manager/view/<account_id>')
def view_account(account_id):
    pass

@app.route('/account-manager/edit/<account_id>', methods=['GET', 'POST'])
def edit_account(account_id):
    account = [account for account in accounts if account['account_id'] == account_id]
    return jsonify({'account' : account})

@app.route('/account-manager/remove/<account_id>', methods=['POST'])
def remove_account(account_id):
    pass

@app.route('/settings', methods=['GET', 'POST'])
@app.route('/settings/', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')


if __name__ == '__main__':
    app.run(debug=True)
