from sqlalchemy import Column, String

from app.mixins import BaseMixin
from app.models import Base


class User(Base, BaseMixin):
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
