from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Depends, status, HTTPException, Response

from .. import schemas, models, utils, oauth2 # this is required if I have pydantic validation schema for login endpoint input
from ..database import get_db
from sqlalchemy.orm import Session

from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    
    tags=['Authentication']
)


@router.post("/login", response_model=schemas.Token)
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
# the above function will work if I use pydantic schema for input validation
# below line is important to remember the semantic for Form Method
# Remember to use form-data in postman
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    #Request form has a field of username which can be anything or even email. so I use this field below
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    print(user_credentials.username)
    print(user_credentials.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    if not utils.hashverify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    # create token
    # return token

    access_token = oauth2.create_token(data = {"user_id": user.id})

    #below dummy return will still match the response_model because of schemas.Token
    # remember the way to pass dummy value has to strictly follow the schema Token
    # return {"access_token": "somevalue", "token_type": "value2"}

    return {"access_token": access_token, "token_type": "bearer"}
    # note that above return is aligned with response model schema of Token class