from flask import Flask, render_template, redirect, url_for, jsonify, request, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv
from sqlmodel import create_engine
from flask_wtf import CSRFProtect
from models import *
from datetime import datetime, date, timezone
from flask_mail import Mail, Message
import datetime, os

load_dotenv('.env')
app = Flask(__name__)
app.config['SECRET_KEY'] =  os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['TEST_EMAIL_ADDRESS'] = os.environ.get('TEST_EMAIL_ADDRESS')
mail = Mail(app)
csrf = CSRFProtect(app)
db_engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='homepage'

class Anon(AnonymousUserMixin):
    def confirm_token(self, token, secret_key, session: Session):
        try:
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return 'Token is expired'
        return True

login_manager.anonymous_user = Anon

@login_manager.user_loader
def load_user(user_id):
    with Session(db_engine) as session:
        return session.exec(select(User).where(User.id == user_id)).one() or None

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.route('/signin', methods=['GET','POST'])
@app.route('/signin/', methods=['GET','POST'])
def signin():
    if request.method == 'POST' and request.form.get('signin'):
      with Session(db_engine) as session:
          user_account = User.check_account_email(request.form.get('email'), session)
          if user_account is not None and user_account.verify_password(request.form.get('password')):
              login_user(user_account, request.form.get('remember_me'))
              next_page = request.args.get('next')
              if next_page is None or not next_page.startswith('/'):
                  next_page = url_for('dashboard')
              return redirect(next_page)
          else:
              flash('Invalid username or password', 'error')
    if request.method == 'POST' and request.form.get('signup'):
        return redirect(url_for('homepage'))
    return render_template('signin.html')


@app.route('/', methods=['GET','POST'])
@app.route('/register', methods=['GET','POST'])
@app.route('/register/', methods=['GET','POST'])
def homepage():
    if request.method == 'POST' and request.form.get('signup'):
        with Session(db_engine) as session:
            user = User(
                name=request.form.get('fullname'),
                email=request.form.get('email'),
                password=request.form.get('password')
            )
            user.register(session)
            token = user.generate_confirmation_token(app.config['SECRET_KEY'])
            user.send_email(
                mail_obj=mail,
                mail={
                    'subject' : 'Account confirmation',
                    'sender' : app.config['MAIL_DEFAULT_SENDER'],
                    'recipient' : request.form.get('email'),
                    'txt_template' : 'email/account_confirmation.txt',
                    'html_template' : 'email/account_confirmation.html'
                },
                user=user,
                token=token
            )
            return redirect(url_for('account_confirmation'))
    if request.method == 'POST' and request.form.get('signin'):
        return redirect(url_for('signin'))
    return render_template('index.html')

@app.route('/account-confirmation')
def account_confirmation():
    return render_template('account_confirmation.html')

@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('dashboard'))
    with Session(db_engine) as session:
        if current_user.confirm_token(token, app.config['SECRET_KEY'], session):
            session.commit()
            return redirect(url_for('account_confirmed'))
        else:
            flash('The confirmation link is invalid or has expired')
        return redirect(url_for('signin'))

@app.route('/confirmed')
def account_confirmed():
    return render_template('confirmed.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
@app.route('/forgot-password/', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        with Session(db_engine) as session:
            user = User.check_account_email(request.form.get('email'), session)
            if user:
                token = user.generate_confirmation_token(app.config['SECRET_KEY'])
                user.send_email(
                    mail_obj=mail,
                    mail={
                        'subject' : 'Reset password',
                        'sender' : app.config['MAIL_DEFAULT_SENDER'],
                        'recipient' : request.form.get('email'),
                        'txt_template' : 'email/forgot_password.txt',
                        'html_template' : 'email/forgot_password.html'
                    },
                    user=user,
                    token=token
                )
                return redirect(url_for('check_email'))
    return render_template('forgot_password.html')


@app.route('/password-reset/<token>')
def reset_token(token):
    with Session(db_engine) as session:
        if current_user.confirm_token(token, app.config['SECRET_KEY'], session):
            return redirect(url_for('change_password'))
        else:
            flash('The token expired')
        return redirect(url_for('forgot_password'))

@app.route('/check-email')
def check_email():
    return render_template('check_email.html')

@app.route('/change-password')
def change_password():
    return render_template('change_password.html')


@app.route('/password-reset')
def password_reset():
    return render_template('password_reset.html')






@app.route('/send-link')
def send_link():
    #route to email link to user
    pass




@app.route('/signout')
@login_required
def signout():
    logout_user()
    flash('You have been signed out')
    return redirect(url_for('signin'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

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
    return render_template('notes.html')

@app.route('/note/view/<note_id>')
def view_note(note_id):
    pass

@app.route('/note/edit/<note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    pass

@app.route('/note/remove/<note_id>', methods=['DELETE'])
def remove_note(note_id):
   pass

@app.route('/account-manager', methods=['GET', 'POST'])
def account_manager():
    return render_template('accounts.html')

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
