import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from flask_login import UserMixin
from linguini.database import Base


class User(Base, UserMixin):
    __tablename__ = 'users'

    username = Column(String(32), primary_key=True, nullable=False)
    password = Column(String, nullable=False)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    pc = Column(Integer, nullable=False)
    role = Column(String(32))

    def __init__(self, username, password, first_name, last_name, pc, role=None):
        self.username = username
        self.password = password

        self.first_name = first_name
        self.last_name = last_name

        self.pc = pc
        self.role = role

    def __repr__(self):
        return '<User username="%r" first_name="%r" last_name="%r">' % (self.username, self.first_name, self.last_name)

    def get_id(self):
        return self.username

    @property
    def fullname(self):
        return self.first_name + ' ' + self.last_name

    @staticmethod
    def get(user_id):
        return User.query.filter_by(username=user_id).first()


class NoticeMixin():
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    # Not nullable but can be blank string technically
    description = Column(String, nullable=False)
    created_date = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False)
    pc = Column(Integer, nullable=False)

    # Optional (nullable)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String)
    attachment_url = Column(String)

    # Foreign Key
    @declared_attr
    def creator_username(cls):
        return Column(String(32), ForeignKey('users.username'), nullable=False)

    @declared_attr
    def creator(cls):
        return relationship('User')


class NoticeModel(NoticeMixin, Base):
    __tablename__ = 'notices'

    def __repr__(self):
        return '<Notice title="%r" creator="%r">' % (self.title, self.creator)


class EventModel(NoticeMixin, Base):
    __tablename__ = 'events'

    payment_url = Column(String)

    def __repr__(self):
        return '<Event title="%r" creator="%r">' % (self.title, self.creator)
