from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

engine = create_engine('sqlite:///instalceu.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    url_name = Column(String(50), nullable=False, unique=True)
    follow_me = Column(Boolean, nullable=True)
    i_follow = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    got_from = Column(String(50), nullable=True)
    
    def __repr__(self):
        return f"<User(name={self.name}, url_name={self.url_name})>"
    
Base.metadata.create_all(engine)