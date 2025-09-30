from os import name
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, Session, select
from datetime import datetime, timezone
from passlib.hash import pbkdf2_sha256
from enum import Enum
import random

class User(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    password: str
    date_added: datetime
    last_active: datetime
    accounts: List['Account'] = Relationship(back_populates='user')
    notes: List['Note'] = Relationship(back_populates='user')

class Account(SQLModel, table=True):
    account_id :int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.user_id', exclude=True)
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





class Note(SQLModel, table=True):
    note_id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.user_id', exclude=True)
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
