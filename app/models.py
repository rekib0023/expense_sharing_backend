import enum

from sqlalchemy import (
    Column,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.mixins import AuditMixin, BaseMixin


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)
metadata = Base.metadata


class User(Base, AuditMixin, BaseMixin):
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)


class ExpenseCategory(Base, AuditMixin, BaseMixin):
    name = Column(String, nullable=False)


class PaidByEnum(enum.Enum):
    Bank = "Bank"
    Card = "Card"
    Cash = "Cash"


class Expense(Base, AuditMixin, BaseMixin):
    name = Column(String, nullable=False)
    paid_by = Column(Enum(PaidByEnum), default=PaidByEnum.Cash, nullable=False)
    amount = Column(Float, default=0.0)
    is_spend = Column(Boolean, default=True, nullable=False)
    category_id = Column(Integer, ForeignKey(ExpenseCategory.id))
    payment_date = Column(DateTime(timezone=True))
    other_details = Column(String, nullable=True)

    category = relationship(
        "ExpenseCategory", foreign_keys="Expense.category_id", lazy="joined"
    )
