'''
Here, the functions sending queries on database are defined
'''
from sqlalchemy.orm import Session

from . import models, schemas

from fastapi import HTTPException

from pydantic import EmailStr

# select user data when user_id is provided
def select_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# select user data when email is provided
def select_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# select user data when username is provided
def select_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# select user data when username and password is provided
def select_user_by_username_and_password(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        user_with_pass = db.query(models.User).filter(models.User.hashed_password == password + "notreallyhashed").first()
        if user_with_pass is not None:
            return user_with_pass
        else:
            raise HTTPException(status_code=403, detail="Incorrecct Password")
# paging can be controlled by controlling variables of skip and limit
def select_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# create a new user in users table, and just populate two fields, email, and password
def insert_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# select items within skip and limit range
def select_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# insert a new row in items table by providing owner_id (as user_id),  and as dictionary {title, description}
def insert_lost_item(db: Session, item: schemas.ItemCreate, email: str):
    db_item = models.Item(**item.dict(), owner_id=email)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
