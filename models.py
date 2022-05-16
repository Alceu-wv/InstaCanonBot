from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

engine = create_engine('sqlite:///instacanon1405.db')
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(63), nullable=True)
    url_name = Column(String(63), nullable=True, unique=True)
    password = Column(String(127), nullable=True)
    last_routine_date = Column(DateTime(timezone=True), nullable=True)
    max_actions_hour = Column(Integer, default=150)
    max_actions_day = Column(Integer, default=500)
    
    def __repr__(self):
        return f">{self.email}< >{self.url_name}<"

class Routine(Base):
    __tablename__ = 'routine'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(63), nullable=True)
    total_actions = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True), default=datetime.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)
    follow_unfollows = Column(Integer, default=0)
    errors = Column(Integer, default=0)
    miss_actions = Column(Integer, default=0)
    report = Column(String(511), nullable=True)
    exception = Column(String(2043), nullable=True)
    
    def __repr__(self):
        return f"<Routine(name={self.name})>"

class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(255), nullable=True)
    url_name = Column(String(255), nullable=False, unique=True)
    follow_me = Column(Boolean, nullable=True)
    i_follow = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now())
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(), nullable=True)
    got_from = Column(String(255), nullable=True)
    __table_args__ = (UniqueConstraint('user_id', 'url_name', name='_user_id_url_name_uc'),)

    
    def __repr__(self):
        return f"<Profile(name={self.name}, url_name={self.url_name})>"
    
Base.metadata.create_all(engine)