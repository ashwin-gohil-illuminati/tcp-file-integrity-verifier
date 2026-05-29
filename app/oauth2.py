
from fastapi import Depends, HTTPException, status

from jose import jwt, JWTError
from datetime import datetime, timedelta

from . import schemas

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') # very important


#SECRET_KEY
#Algorithm
#Expiration time

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_token(data: dict):

    # here data is variable of type dict which contains fields passed to it which is put in payload
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt)

    return encoded_jwt


def verify_token(inputtoken: str, credentials_exception):

    try:

       payload = jwt.decode(inputtoken, SECRET_KEY, algorithms=[ALGORITHM])

       id:str = payload.get("user_id") # as encoded is in form of name value pairs, a dictionary

       if id is None:
           raise credentials_exception

       token_data = schemas.TokenData(id=id) # this is important and note that indentation was strict. it created error
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(inputtoken: str = Depends(oauth2_scheme)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail=f"could not validate credentials",
                                           headers={"WWW-Authenticate": "Bearer"})

    return verify_token(inputtoken, credentials_exception)
