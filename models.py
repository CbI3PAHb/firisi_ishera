from sqlalchemy import Boolean, Column, Integer, String

from database import Base 

class Flowers_db(Base):
    __tablename__ = "predicts"

    id = Column(Integer, primary_key=True, index=True)
    input = Column(String)
    output = Column(String)