from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr



class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class AllUsers(BaseModel):
   
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class ConnectionInfo(BaseModel):
    ip: str
    port: int
    instruction: str
    note: str

class ConnectionDescription(BaseModel):
    jobdescription: str
    jobid: Optional[int] = None

class ScanResult(BaseModel):
    filename: str
    filepath: str
    hash: str
    jobid: int
    jobdescription: str
    created_at: datetime

    class Config:
        orm_mode = True

class RescanResult(BaseModel):
    filename: str
    filepath: str
    hash: str
    latesthash: str
    altered: bool
    jobid: int
    jobdescription: str
    created_at: datetime

    class Config:
        orm_mode = True

class ScanJobs(BaseModel):
    jobid: int
    jobdescription: str

    class Config:
        orm_mode = True

class DeleteScanJobs(BaseModel):
    jobid: int


    
