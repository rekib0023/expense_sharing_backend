import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.mixins import AuditMixin, BaseMixin
from app.models import Base
from app.models.user_model import User


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


class ExpenseGroup(Base, AuditMixin, BaseMixin):
    name = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey(User.id))

    owner = relationship("User", foreign_keys="ExpenseGroup.owner_id", lazy="joined")


class ExpenseGroupUser(Base, AuditMixin, BaseMixin):
    user_id = Column(Integer, ForeignKey(User.id))
    group_id = Column(Integer, ForeignKey(ExpenseGroup.id))

    user = relationship("User", foreign_keys="ExpenseGroupUser.user_id", lazy="joined")
    group = relationship(
        "ExpenseGroup", foreign_keys="ExpenseGroupUser.group_id", lazy="joined"
    )


class Friends(Base, AuditMixin, BaseMixin):
    user_id = Column(Integer, ForeignKey(User.id))
    friend_id = Column(Integer, ForeignKey(User.id))

    user = relationship("User", foreign_keys="Friends.user_id", lazy="joined")
    friend = relationship("User", foreign_keys="Friends.friend_id", lazy="joined")
