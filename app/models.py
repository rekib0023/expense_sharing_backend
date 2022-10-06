import enum

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship

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


class PaymentTypeEnum(enum.Enum):
    Bank = "Bank"
    Card = "Card"
    Cash = "Cash"


class Expense(Base, AuditMixin, BaseMixin):
    name = Column(String, nullable=False)
    type = Column(Enum(PaymentTypeEnum), default=PaymentTypeEnum.Cash, nullable=False)
    amount = Column(Float, default=0.0)
    category_id = Column(Integer, ForeignKey(ExpenseCategory.id))

    category = relationship(
        "ExpenseCategory", foreign_keys="Expense.category_id", lazy="joined"
    )
