from flask import jsonify
from os import name
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, Session, select
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from passlib.hash import pbkdf2_sha256
from enum import Enum


class User(SQLModel, table=True):
    __tablename__ = 'users'
    user_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    password: str
    date_added: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_active: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    accounts: List['Account'] = Relationship(back_populates='user')
    notes: List['Note'] = Relationship(back_populates='user')

    def __init__(self, name: str, email: str, password: str):
       self.name = name
       self.email = email
       self.password = password
       self.date_added = datetime.now(timezone.utc)
       self.last_active = datetime.now(timezone.utc)

    def register(self, session: Session):
        try:
            self.password = pbkdf2_sha256.hash(self.password)
            session.add(self)
            session.commit()
            session.refresh(self)
            return self
        except IntegrityError as e:
            raise ValueError('Registration failed') from e

    def _verify_password(self, password: str):
        return pbkdf2_sha256.verify(password, self.password)

    def check_account(self, password, page_template):
        if self._verify_password(password):
            return page_template['dashboard']
        return page_template['sign in']

    def send_email(self, email, mail, page_template):
        email.html = page_template
        mail.send(email)
        return jsonify({'status' : 200})


class Account(SQLModel, table=True):
    account_id : Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key='users.user_id', exclude=True)
    name: str
    mobile: str
    email: str = Field(unique=True)
    password: str
    date_added: datetime
    due_date: datetime
    amount: int
    category: str
    note: str | None = None
    user: Optional[User] = Relationship(back_populates='accounts')

    def __init__(self, name: str, email: str, password: str, mobile: str, amount: int , category: str, note: str):
        self.name = name
        self.email = email
        self.password = password
        self.mobile = mobile
        self.amount = amount
        self.category = category
        self.note = note
        self.date_added = datetime.now(timezone.utc)
        self.due_date = datetime.now(timezone.utc)





class Note(SQLModel, table=True):
    note_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key='users.user_id', exclude=True)
    title: str
    note: str
    category: str
    date_added: datetime
    user: Optional[User] = Relationship(back_populates='notes')

    def __init__(self, title: str, note: str, category: str):
       self.title = title
       self.note = note
       self.category = category




class CharacterOptions(Enum):
    LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ALPHANUMERIC = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    NUMBERS = '0123456789'
    ALPHANUMERIC_SPECIAL= 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-=+$@#!~^%*(?<)>'

class Utilities:
    @classmethod
    def password_generator(cls, password_length: int, characters_option : CharacterOptions) -> str:
        characters = characters_option.value
        password_result = [random.choice(characters)for _ in range(int(password_length))]
        return ''.join(password_result)
