from typing import List
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
import schemas, models
from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user with id '{user_id}' found in database")

    return user

@app.get('/users/', response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users

@app.put('/users/', response_model=schemas.User)
def update_user(request: schemas.User, db: Session = Depends(get_db)):
        
    user = db.query(models.User).filter(models.User.id == request.id)
    user.update(request.dict())
    db.commit()
    response = user.first()
    
    return response

@app.post('/users/', response_model=schemas.User)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user = models.User(email=request.email, f_name=request.f_name, l_name=request.l_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.delete('/users/', response_model=schemas.UserDelete)
def delete_user(request: schemas.UserDelete, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email '{request.email}' not found in database")
    
    db.delete(user)
    db.commit()

    return user





