import database
import models
import sqlalchemy.orm as orm
import schemas
from datetime import datetime

def create_database():
    return database.Base.metadata.create_all(bind=database.engine)

def get_db():
    with database.SessionLocal() as db:
        yield db

def get_user_by_email(db: orm.Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: orm.Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "thisisnotsecure"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: orm.Session, skip: int, limit: int):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: orm.Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_post(db: orm.Session, post: schemas.PostCreate, user_id: int):
    post = models.Post(**post.dict(), owner_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_posts(db: orm.Session, skip: int, limit: int):
    return db.query(models.Post).offset(skip).limit(limit).all()

def get_post(db: orm.Session, post_id: int):
    return db.query(models.Post).filter(models.Post.post_id == post_id).first()

def delete_post(db: orm.Session, post_id: int):
    db.query(models.Post).filter(models.Post.post_id == post_id).delete()
    db.commit()

def update_post(db: orm.Session, post: schemas.PostCreate, post_id: int):
    db_post = get_post(db=db, post_id=post_id)
    # db_post.__dict__.update(**post)
    db_post.title = post.title
    db_post.content = post.content
    db_post.date_last_created = datetime.now()
    db.commit()
    db.refresh(db_post)
    return db_post

