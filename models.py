from flask import jsonify, render_template
from flask_login import UserMixin, AnonymousUserMixin
from os import name
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, Session, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from datetime import datetime, timezone, date, timedelta
from flask_mail import Message
from threading import Thread
from passlib.hash import pbkdf2_sha256
from email_validator import validate_email, EmailNotValidError
from app import app, mail
from enum import Enum
from uuid import UUID, uuid4
import random
import jwt

class User(SQLModel, UserMixin, table=True):
    __tablename__ = 'users'
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    email: str = Field(unique=True)
    password: str = Field(default=None)
    date_added: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_active: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    confirmed: bool = Field(default=False)
    accounts: List['Account'] = Relationship(back_populates='user')
    notes: List['Note'] = Relationship(back_populates='user')
    tokens: List['Token'] = Relationship(back_populates='user')

    def __init__(
        self,
        email: str,
        password: str,
        name=None,
        id:  Optional[int] =  None
    ):
       self.name = name
       self.email = email
       self.password = password
       self.date_added = datetime.now(timezone.utc)
       self.last_active = datetime.now(timezone.utc)
       self.id = id

    def register(self, session: Session):
        try:
            self.password = pbkdf2_sha256.hash(self.password)
            session.add(self)
            session.commit()
            session.refresh(self)
            return self
        except IntegrityError as e:
            session.rollback()
            raise ValueError('Registration failed') from e

    def verify_password(self, password: str):
        return pbkdf2_sha256.verify(password, self.password)

    @classmethod
    def check_account_email(cls, email: str, session: Session):
        try:
            return session.exec(select(User).where(User.email == email)).one()
        except NoResultFound:
            return None

    def validate_account_email(self):
        try:
            user_email = validate_email(self.email, check_deliverability=True)
            return user_email.email
        except EmailNotValidError as e:
            return f"Invalid email address: {e}"

    @staticmethod
    def compare_passwords(password, confirm_password):
        if password == confirm_password:
            return True

    @staticmethod
    def _send_async(app, message):
       with app.app_context():
           mail.send(message)

    def send_email(self, mail_obj, mail, **kwargs):
        message = Message(
            subject=mail['subject'],
            sender=mail['sender'],
            recipients=[mail['recipient']]
        )
        message.body = render_template(mail['txt_template'], **kwargs)
        message.html = render_template(mail['html_template'], **kwargs)
        thr = Thread(target=User._send_async, args=[app, message])
        thr.start()
        return thr

    def retrieve(self, session: Session):
        try:
            return session.exec(select(User).where(User.id == self.id)).one()
        except Exception as e:
            raise ValueError('Unable to retrieve user') from e

    def generate_confirmation_token(self, secret_key):
        current_time = datetime.now(timezone.utc) + timedelta(minutes=15)
        token = jwt.encode({'user_id' : self.id, 'exp' : current_time}, secret_key, algorithm='HS256')
        return token

    def confirm_token(self, token, secret_key, session: Session):
        try:
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return 'Token is expired'
        if data['user_id'] != self.id:
            return False
        self.confirmed = True
        session.add(self)
        return True


class Token(SQLModel, table=True):
    __tablename__ = 'tokens'
    token_id: Optional[int] = Field(default=None, primary_key=True)
    token_type: str = Field(default='Remember me')
    token: UUID = Field(default_factory=uuid4, unique=True,index=True)
    user_id: Optional[int] = Field(default=None, foreign_key='users.id')
    user: User = Relationship(back_populates='tokens')

class Account(SQLModel, table=True):
    __tablename__ = 'accounts'
    account_id : Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key='users.id', exclude=True)
    name: str
    mobile: str
    email: str = Field(unique=True)
    password: str
    date_added: datetime
    due_date: date
    amount: int
    category: str
    note: str | None = None
    user: Optional[User] = Relationship(back_populates='accounts')

    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        mobile: str,
        amount: int ,
        category: str,
        note: str,
        due_date: date,
        user_id: Optional[int] = None,
        account_id: Optional[int] = None
    ):
            self.name = name
            self.email = email
            self.password = password
            self.mobile = mobile
            self.amount = amount
            self.category = category
            self.note = note
            self.date_added = datetime.now(timezone.utc)
            self.due_date = due_date
            self.user_id = user_id
            self.account_id = account_id

    def add(self, session: Session):
        try:
            session.add(self)
            session.commit()
            session.refresh(self)
            return self
        except:
            session.rollback()
            return 'Unable to save account'

    def retrieve_one(self, session: Session):
       try:
           return session.exec(select(Account).where(Account.account_id == self.account_id)).one()
       except Exception as e:
           raise ValueError('Unable to retrieve account') from e

    def retrieve_all(self, session: Session):
        try:
           results = session.exec(select(Account).where(Account.user_id == self.user_id))
           return [accounts for accounts in results]
        except Exception as e:
            raise ValueError('Unable to retrieve accounts') from e

    def update(self, session: Session):
        try:
            session.add(self)
            session.commit()
            session.refresh(self)
            return self
        except IntegrityError as e:
            session.rollback()
            raise ValueError('Unable to update account') from e

    def remove(self, session: Session):
        try:
            session.delete(self)
            session.commit()
            return "Account item removed"
        except IntegrityError as e:
            session.rollback()
            raise ValueError('Unable to remove account item') from e



class Note(SQLModel, table=True):
    __tablename__ = 'notes'
    note_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key='users.id', exclude=True)
    title: str
    note: str
    category: str
    date_added: datetime
    user: Optional[User] = Relationship(back_populates='notes')

    def __init__(self,
        title: str,
        note: str,
        category: str,
        note_id: Optional[int] = None,
        user_id: Optional[int] = None
    ):
       self.title = title
       self.note = note
       self.category = category
       self.date_added = datetime.now(timezone.utc)
       self.note_id = note_id
       self.user_id = user_id

    def add(self, session: Session):
        try:
            session.add(self)
            session.commit()
            session.refresh(self)
            return self
        except IntegrityError as e:
            session.rollback()
            raise ValueError('Unable to save note') from e

    def retrieve_one(self, session: Session):
        try:
            return session.exec(select(Note).where(Note.note_id == self.note_id)).one()
        except Exception as e:
            raise ValueError('Unable to retrieve note') from e

    def retrieve_all(self, session: Session):
        try:
           result = session.exec(select(Note).where(Note.user_id == self.user_id))
           return [notes for notes in result]
        except Exception as e:
            raise ValueError('Unable to retrieve notes') from e

    def update(self, session: Session):
        try:
            session.add(self)
            session.commit()
            session.refresh(self)
            return self
        except IntegrityError as e:
            session.rollback()
            raise ValueError('Unable to update note') from e

    def remove(self, session: Session):
        try:
            session.delete(self)
            session.commit()
            return 'Note removed'
        except IntegrityError as e:
            session.rollback()
            raise ValueError('Unable to remove note') from e


class CharacterOptions(Enum):
    LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ALPHANUMERIC = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    NUMBERS = '0123456789'
    ALPHANUMERIC_SPECIAL= 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-=+$@#!~^%*(?<)>'

class Utilities:
    @staticmethod
    def password_generator(password_length: int, characters_option : CharacterOptions) -> str:
        characters = characters_option.value
        password_result = [random.choice(characters)for _ in range(int(password_length))]
        return ''.join(password_result)

    @staticmethod
    def generate_uuid():
        ''' Generate uuid in a format that excludes hypens '''
        import uuid
        return str(uuid.uuid4()).replace('-', '')
