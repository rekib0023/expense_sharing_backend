from typing import Dict, List, Union

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_

from .. import oauth2, schemas
from ..models import expense_model

router = APIRouter()


@router.post(
    "/category",
    summary="Creates a new expense category",
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    request: Request,
    payload: schemas.CreateExpenseCategory,
):
    try:
        category = expense_model.ExpenseCategory.create(**payload.dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return category


@router.get(
    "/categories",
    summary="Get all expense categories",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ExpenseCategory],
)
def get_categories(
    request: Request,
):
    try:
        categories = expense_model.ExpenseCategory.query().all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return categories


@router.get(
    "/category/{id}",
    summary="Get all expense categories",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ExpenseCategory,
)
def get_category(
    request: Request,
    id,
):
    try:
        category = expense_model.ExpenseCategory.get(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return category


@router.post(
    "/",
    summary="Creates a new expense",
    status_code=status.HTTP_201_CREATED,
)
def create_expense(
    request: Request,
    payload: schemas.CreateExpense,
):
    try:
        payload.amount = (0 - payload.amount) if payload.is_spend else payload.amount
        expense = expense_model.Expense.create(**payload.dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return expense


@router.get(
    "/",
    summary="Get all expenses",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Expense],
)
def get_expenses(
    request: Request,
    type: Union[str, None] = None,
    value: Union[str, None] = None,
    amount_gt: Union[int, None] = None,
    amount_lt: Union[int, None] = None,
):
    if type and type not in ["category", "paid_by"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filter type. Must be of category, paid_by.",
        )
    filters = []

    if type == "category":
        category = expense_model.ExpenseCategory.get_by(name=value)
        if category:
            category_id = category.id
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No category found for the given filter",
            )
        filters.append(expense_model.Expense.category_id == category_id)
    elif type == "type":
        filters.append(expense_model.Expense.type == value)

    if amount_gt and amount_lt:
        filters.append(expense_model.Expense.amount >= amount_gt)
        filters.append(expense_model.Expense.amount <= amount_lt)
    elif amount_gt:
        filters.append(expense_model.Expense.amount >= amount_gt)
    elif amount_lt:
        filters.append(expense_model.Expense.amount <= amount_lt)

    try:
        if filters:
            expenses = (
                expense_model.Expense.query()
                .filter(and_(el for el in filters))
                .order_by(expense_model.Expense.payment_date.desc())
            )
        else:
            expenses = (
                expense_model.Expense.query().order_by(
                    expense_model.Expense.payment_date.desc()
                )
                # .filter(models.Expense.cre)
                .all()
            )

        expenses = [jsonable_encoder(e) for e in expenses]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return expenses


@router.delete(
    "/{id}", summary="Delete an expense", status_code=status.HTTP_204_NO_CONTENT
)
def delete_expense(
    request: Request,
    id,
):
    expense = expense_model.Expense.get(id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found.",
        )
    try:
        expense.delete()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return "Deleted successfully"


@router.put("/{id}", summary="Update an expense", status_code=status.HTTP_200_OK)
def update_expense(
    request: Request,
    id,
    payload: schemas.CreateExpense,
):
    expense = expense_model.Expense.get(id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found.",
        )
    try:
        payload.amount = (0 - payload.amount) if payload.is_spend else payload.amount
        expense.name = payload.name
        expense.paid_by = payload.paid_by
        expense.amount = payload.amount
        expense.is_spend = payload.is_spend
        expense.payment_date = payload.payment_date
        expense.other_details = payload.other_details
        expense.category_id = payload.category_id
        expense.save()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return expense


@router.get(
    "/group",
    summary="Get expenses in group",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, List[schemas.ExpenseByGroup]],
)
def get_expenses_group(
    request: Request,
    by: str,
):
    if by and by not in ["category", "paid_by"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filter. Must be of category, paid_by.",
        )
    try:
        expenses = expense_model.Expense.query().all()
        expenses = [jsonable_encoder(e) for e in expenses]

        result = {}
        for e in expenses:
            temp = e.pop(by)
            if by == "category":
                temp = temp["name"]
            if temp not in result:
                result[temp] = []
            result[temp].append(e)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/{id}",
    summary="Get all expenses",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Expense,
)
def get_expense(
    request: Request,
    id,
):
    expense = expense_model.Expense.get(id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found.",
        )
    try:
        expense = jsonable_encoder(expense)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return expense
