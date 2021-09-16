import fastapi
import services
import schemas
import sqlalchemy.orm as orm
from typing import List
app = fastapi.FastAPI()
services.create_database()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: orm.Session=fastapi.Depends(services.get_db)):
    db_user = services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail="Oops, the email is in use")
    return services.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int=0, limit: int=10, db: orm.Session=fastapi.Depends(services.get_db)):
    users = services.get_users(db=db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: orm.Session=fastapi.Depends(services.get_db)):
    db_user = services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise fastapi.HTTPException(status_code=404, detail="This user does not exists")
    return db_user

@app.post("/users/{user_id}/posts", response_model=schemas.Post)
def create_post(user_id: int, post: schemas.Post, db: orm.Session=fastapi.Depends(services.get_db)):
    db_user = services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise fastapi.HTTPException(status_code=404, detail="This user does not exists")
    return create_post(db=db, post=post, user_id=user_id)
    
@app.get("/posts/", response_model=List[schemas.Post])
def read_posts(skip: int=0, limit: int=10, db: orm.Session=fastapi.Depends(services.get_db)):
    return services.get_posts(db=db, skip=skip, limit=limit)

@app.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: orm.Session=fastapi.Depends(services.get_db)):
    post = services.get_post(db=db, post_id=post_id)
    if post is None:
        raise fastapi.HTTPException(status_code=404, detail="This post does not exists")
    return post

@app.delete("posts/{post_id}")
def delete_post(post_id: int, db: orm.Session=fastapi.Depends(services.get_db)):
    services.delete_post(db=db, post_id=post_id)

@app.put("/posts/{post_id}")
def update_post(post_id: int, post: schemas.PostCreate, db: orm.Session=fastapi.Depends(services.get_db)):
    return services.update_post(db=db, post=post, post_id=post_id)