import sqlalchemy as sql
import sqlalchemy.orm as orm
from datetime import datetime

import database

class User(database.Base):
    __tablename__ = "users"
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    email = sql.Column(sql.String, unique=True)
    hashed_password = sql.Column(sql.String)
    is_active = sql.Column(sql.Boolean, default=True)

    posts = orm.relationship("Post", back_populates="owner")

class Post(database.Base):
    __tablename__ = "posts"
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    title = sql.Column(sql.String, index=True)
    content = sql.Column(sql.String, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    date_created = sql.Column(sql.DateTime, default=datetime.utcnow)
    date_last_created = sql.Column(sql.DateTime, default=datetime.utcnow)

    owner = orm.relationship("User", back_populates="posts")
    
