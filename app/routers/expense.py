from typing import Dict, List, Union
from sqlalchemy import and_

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from .. import models, oauth2, schemas

router = APIRouter()
from fastapi.encoders import jsonable_encoder


@router.post(
    "/category",
    summary="Creates a new expense category",
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    payload: schemas.CreateExpenseCategory,
    _: str = Depends(oauth2.require_user),
):
    try:
        category = models.ExpenseCategory.create(**payload.dict())
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
def get_categories(_: str = Depends(oauth2.require_user)):
    try:
        categories = models.ExpenseCategory.query().all()
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
def get_category(id, _: str = Depends(oauth2.require_user)):
    try:
        category = models.ExpenseCategory.get(id)
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
    payload: schemas.CreateExpense, _: str = Depends(oauth2.require_user)
):
    try:
        expense = models.Expense.create(**payload.dict())
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
    type: Union[str, None] = None,
    value: Union[str, None] = None,
    amount_gt: Union[int, None] = None,
    amount_lt: Union[int, None] = None,
    _: str = Depends(oauth2.require_user),
):
    if type and type not in ["category", "type"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filter type. Must be of category, type.",
        )
    filters = []

    if type == "category":
        category = models.ExpenseCategory.get_by(name=value)
        if category:
            category_id = category.id
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No category found for the given filter",
            )
        filters.append(models.Expense.category_id == category_id)
    elif type == "type":
        filters.append(models.Expense.type == value)

    if amount_gt and amount_lt:
        filters.append(models.Expense.amount >= amount_gt)
        filters.append(models.Expense.amount <= amount_lt)
    elif amount_gt:
        filters.append(models.Expense.amount >= amount_gt)
    elif amount_lt:
        filters.append(models.Expense.amount <= amount_lt)

    try:
        if filters:
            expenses = models.Expense.query().filter(and_(el for el in filters))
        else:
            expenses = models.Expense.query().all()

        expenses = [jsonable_encoder(e) for e in expenses]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return expenses


@router.get(
    "/group",
    summary="Get expenses in group",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, List[schemas.ExpenseGroup]],
)
def get_expenses_group(by: str, _: str = Depends(oauth2.require_user)):
    if by and by not in ["category", "type"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filter. Must be of category, type.",
        )
    try:
        expenses = models.Expense.query().all()
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
def get_expense(id, _: str = Depends(oauth2.require_user)):
    try:
        expense = models.Expense.get(id)
        expense = jsonable_encoder(expense)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return expense
