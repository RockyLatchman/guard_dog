from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, Session, select
from datetime import datetime, timezone
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
    note: str
    user: Optional[User] = Relationship(back_populates='accounts')

class Note(SQLModel, table=True):
    note_id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.user_id', exclude=True)
    title: str
    note: str
    category: str
    date_added: datetime
    user: Optional[User] = Relationship(back_populates='notes')

class CharacterOptions(Enum):
    LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ALPHANUMERIC = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    NUMBERS = '0123456789'
    ALPHANUMERIC_SPECIAL= 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-=+$@#!~^%*(?<)>'

class Utilities:
    @classmethod
    def password_generator(cls, password_length: int, characters_option : CharacterOptions) -> str:
        characters = characters_option.value
        password_result = [random.choice(characters)for _ in range(password_length)]
        return ''.join(password_result)
