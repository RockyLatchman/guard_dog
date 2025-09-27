from flask import Flask, render_template, redirect, url_for
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv
from sqlmodel import create_engine
from models import *
import os

load_dotenv('.env')
app = Flask(__name__)
app.config['SECRET_KEY'] =  os.environ.get('SECRET_KEY')
db_engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))

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
    pass

@app.route('/reset-password')
def reset_password():
    pass

@app.route('/signout')
def signout():
    pass

@app.route('/password-generator')
def password_gen():
    pass

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    pass

@app.route('/note/view/<note_id>')
def view_note(note_id):
    pass

@app.route('/note/edit/<note_id>', methods=['PUT'])
def edit_note(note_id):
    pass

@app.route('/note/remove/<note_id>', methods=['DELETE'])
def remove_note(note_id):
   pass

@app.route('/account-manager', methods=['GET', 'POST'])
def account_manager():
    pass

@app.route('/account-manager/view/<account_id>')
def view_account(account_id):
    pass

@app.route('/account-manager/edit/<account_id>', methods=['PUT'])
def edit_account(account_id):
    pass

@app.route('/account-manager/remove/<account_id>', methods=['DELETE'])
def remove_account(account_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)
