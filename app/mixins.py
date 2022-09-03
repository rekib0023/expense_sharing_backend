from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
# from app.dependency import get_current_user\\
from db import get_db
from fastapi import HTTPException


db = next(get_db())

class AuditMixin(object):
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # @declared_attr
    # def created_by_id(cls):
    #     return Column(Integer,
    #         ForeignKey('user.id', name='fk_%s_created_by_id' % cls.__name__, use_alter=True),
    #         # nullable=False,
    #         default=_current_user_id_or_none
    #     )

    # @declared_attr
    # def created_by(cls):
    #     return relationship(
    #         'User',
    #         primaryjoin='User.id == %s.created_by_id' % cls.__name__,
    #         remote_side='User.id'
    #     )

    # @declared_attr
    # def updated_by_id(cls):
    #     return Column(Integer,
    #         ForeignKey('user.id', name='fk_%s_updated_by_id' % cls.__name__, use_alter=True),
    #         # nullable=False,
    #         default=_current_user_id_or_none,
    #         onupdate=_current_user_id_or_none
    #     )

    # @declared_attr
    # def updated_by(cls):
    #     return relationship(
    #         'User',
    #         primaryjoin='User.id == %s.updated_by_id' % cls.__name__,
    #         remote_side='User.id'
    #     )




class BaseMixin(object):
    _repr_hide = ['created_at', 'updated_at']

    @classmethod
    def query(cls):
        return db.query(cls)

    @classmethod
    def get(cls, id):
        return cls.query().get(id)

    @classmethod
    def get_by(cls, **kw):
        return cls.query().filter_by(**kw).first()

    @classmethod
    def get_or_404(cls, id):
        rv = cls.get(id)
        if rv is None:
            raise HTTPException(status_code=404, detail=f"Item {cls.__name__} not found")
        return rv

    @classmethod
    def get_or_create(cls, **kw):
        r = cls.get_by(**kw)
        if not r:
            r = cls(**kw)
            db.add(r)
            db.commit()
            db.refresh(cls)

        return r

    @classmethod
    def create(cls, **kw):
        r = cls(**kw)
        db.add(r)
        db.commit()
        db.refresh(cls)
        return r

    def save(self):
        db.add(self)
        db.commit()
        db.refresh(self)

    def delete(self):
        db.delete(self)
        db.commit()
        db.refresh(self)

    def __repr__(self):
        values = ', '.join("%s=%r" % (n, getattr(self, n)) for n in self.__table__.c.keys() if n not in self._repr_hide)
        return "%s(%s)" % (self.__class__.__name__, values)

    def filter_string(self):
        return self.__str__()


# async def _current_user_id_or_none():
#     try:
#         return await get_current_user().id
#     except:
#         return None