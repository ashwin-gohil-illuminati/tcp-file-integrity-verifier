

from sqlalchemy import TIMESTAMP, Column, Integer
from .database import Base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.schema import Sequence


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

"""
class Port(Base):
    __tablename__ = "ports"

    userid = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    seq = Sequence('article_aid_seq', start=3000)   #article_aid_seq
    portno = Column('portno', Integer, seq, server_default=seq.next_value())
    jobdone = Column(Boolean, server_default='False', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
"""

class Port(Base):
    __tablename__ = "ports"

    userid = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    portno = Column(Integer, nullable=False)
    jobdone = Column(Boolean, server_default='False', nullable=False)
    jobdescription = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
class HashData(Base):
    __tablename__ = "hashdata"

    id = Column(Integer, primary_key=True, nullable=False)
    userid = Column(Integer, nullable=False)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    jobid = Column(Integer, nullable=False)
    jobdescription = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class HashDataRescan(Base):
    __tablename__ = "hashdatarescan"

    id = Column(Integer, primary_key=True, nullable=False)
    userid = Column(Integer, nullable=False)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    latesthash = Column(String, nullable=False)
    altered = Column(Boolean, nullable = False)
    jobid = Column(Integer, nullable=False)
    jobdescription = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))
