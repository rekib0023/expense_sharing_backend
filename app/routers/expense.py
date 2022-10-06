from typing import List

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
        print(payload)
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
def get_expenses(_: str = Depends(oauth2.require_user)):
    try:
        expenses = models.Expense.query().all()
        expenses = [jsonable_encoder(e) for e in expenses]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return expenses


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
