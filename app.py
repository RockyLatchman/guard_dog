from flask import Flask, render_template, redirect, url_for
from passlib.hash import pbkdf2_sha256
from .models import *

app = Flask(__name__)

@app.route('/')
def homepage():
    pass

@app.route('/register', methods=['POST'])
def register():
    pass

@app.route('/signin', methods=['POST'])
def signin():
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
    app.run()
