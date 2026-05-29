from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Response, status, HTTPException, Depends

from ..database import get_db
from sqlalchemy.orm import Session

from .. import schemas, utils, models, oauth2

from typing import List

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password 

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    checkuser = db.query(models.User).filter(models.User.email == user.email).first()
    if checkuser:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"User already exists")

    new_user = models.User(**user.dict()) # this is important line, unpacking
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[schemas.AllUsers])
def get_users(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    # This is important here as output of response_model which is a pydantic class for validation
    # This is required but output is in form of a List so List[schemas.AllUsers] will be required
    # I have removed the password field in the output by declaring schema class attributes

    allusers = db.query(models.User).all()
    
    print(allusers[1].id)
    
    return allusers