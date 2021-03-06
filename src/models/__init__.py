from flask_sqlalchemy import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, \
    MetaData, Table, LargeBinary, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import scoped_session, sessionmaker

import enum
import json
import os

engine = create_engine(os.environ.get('POSTGRESQL_DB_URL'), convert_unicode = True)
db_session = scoped_session(sessionmaker(autocommit = False, autoflush = False, bind = engine))

Base = declarative_base()
Base.query = db_session.query_property()

tags_assets = Table('tags_assets', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id')),
    Column('asset_id', Integer, ForeignKey('assets.id')),
    UniqueConstraint('tag_id', 'asset_id', name = 'uix_1')
)

class ManagementStatus(enum.Enum):
    APPROVED = 1
    REJECTED = 2

class Asset(Base):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String(255), unique = True, nullable = False)
    tags = relationship('Tag', secondary = tags_assets,
        backref = backref('assets', lazy = 'dynamic'))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, nullable = False)
    handle = Column(String(255), unique = True, nullable = False)
    email = Column(String(255), unique = True, nullable = False)
    phone = Column(String(255), unique = False, nullable = True)
    gchat_handle = Column(String(255), unique = False, nullable = True)

class Upload(Base):
    __tablename__ = 'uploads'
    id = Column(Integer, primary_key = True, unique = True, nullable = False)
    asset = Column(Integer, ForeignKey('assets.id'), name = 'asset_id', nullable = False)
    user = Column(Integer, ForeignKey('users.id'), name = 'user_id', nullable = False)
    title = Column(String(255), nullable = False)
    file_extension = Column(String(255), nullable = False)
    thumbnail = LargeBinary(length = 1024 * 1024 * 2)
    management_status = Column(Integer, nullable = True)
    management_comment = Column(String(255), nullable = False)

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String(255), unique = True, nullable = False)

class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key = True, nullable = False)
    upload = Column(Integer, ForeignKey('uploads.id'), name = 'upload_id', nullable = False)
    author = Column(Integer, ForeignKey('users.id'), name = 'author_id', nullable = False)
    rating = Column(Integer, nullable = True)
    text = Column(String(1024 * 8), unique = False, nullable = True)
