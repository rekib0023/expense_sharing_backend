from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class BaseCls(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=BaseCls)
metadata = Base.metadata
