from datetime import datetime
from typing import List, Literal, Union

from pydantic import BaseModel, EmailStr, constr


class UserBaseSchema(BaseModel):
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class MyBaseModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime = None


class UserResponse(UserBaseSchema, MyBaseModel):
    pass


class CreateExpenseCategory(BaseModel):
    name: str


class ExpenseCategory(CreateExpenseCategory):
    id: int

    class Config:
        orm_mode = True


class ExpenseBase(BaseModel):
    name: str
    paid_by: Literal["Bank", "Card", "Cash"] = None
    amount: float
    is_spend: Union[bool, None] = True
    payment_date: datetime = None
    other_details: str = None


class CreateExpense(ExpenseBase):
    category_id: int


class Expense(ExpenseBase, MyBaseModel):
    id: int
    category: ExpenseCategory


class ExpenseByGroup(BaseModel):
    id: int
    name: str
    amount: float
    category: Union[ExpenseCategory, None]
    paid_by: Union[str, None]
    is_spend: bool
    payment_date: datetime = None
    other_details: str


class CreateExpenseGroup(BaseModel):
    name: str
    desc: str
    owner_id: int
    group_user_ids: List[int]
