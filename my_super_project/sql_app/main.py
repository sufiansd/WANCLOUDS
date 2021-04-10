'''
Here core functions are defined for different operations, and the functions make
calls to the crud functions.
'''

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from pydantic import EmailStr

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create user account with fields email, username and password by calling crud.insert_user function
@app.post("/users/", response_model=schemas.User)
def create_account(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # check if the user's email is already present in table or not
    db_user = crud.select_user_by_email(db, email=user.email)
    # if the user is already registered
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # if user is not already registered (his email is not in table)
    return crud.insert_user(db=db, user=user)

# read all users from users table by calling crud.select_users function
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.select_users(db, skip=skip, limit=limit)
    return users


# get user data by user_id by calling crud.select_user_by_id method
@app.get("/users/{username}", response_model=schemas.User)
def login(username: str, password: str, db: Session = Depends(get_db)):
    #db_user = crud.select_user_by_username(db, username=username)
    db_user_pass = crud.select_user_by_username_and_password(db, username=username, password = password)
    if db_user_pass is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user_pass


# insert an item for user
@app.post("/users/{email}/items/", response_model=schemas.Item)
def insert_lost_item(
    email: str, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.insert_lost_item(db=db, item=item, email=email)

# get all items 
@app.get("/items/", response_model=List[schemas.Item])
def view_lost_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.select_items(db, skip=skip, limit=limit)
    return items


