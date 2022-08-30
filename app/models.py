from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String,)
    last_name = Column(String)
    email = Column(String)
    hashed_password = Column(String)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name