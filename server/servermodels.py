from sqlalchemy import TIMESTAMP, Column, Integer
from serverdatabase import Base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.schema import Sequence



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