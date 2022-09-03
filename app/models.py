from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from app.mixins import AuditMixin, BaseMixin


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    id =  Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)
metadata = Base.metadata


class User(Base, AuditMixin, BaseMixin):
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)