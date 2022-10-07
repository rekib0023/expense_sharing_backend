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


class UserResponse(UserBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime = None


class CreateExpenseCategory(BaseModel):
    name: str


class ExpenseCategory(CreateExpenseCategory):
    id: int

    class Config:
        orm_mode = True


class ExpenseBase(BaseModel):
    name: str
    type: Literal["Bank", "Card", "Cash"]
    amount: float


class CreateExpense(ExpenseBase):
    category_id: int


class Expense(ExpenseBase):
    id: int
    category: ExpenseCategory


class ExpenseGroup(BaseModel):
    id: int
    name: str
    amount: float
    category: Union[ExpenseCategory, None]
    type: Union[str, None]
    # __root__: Union[str, ExpenseCategory]
