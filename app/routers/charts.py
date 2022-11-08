from fastapi import APIRouter, HTTPException, Request, status
from sqlalchemy import and_

from ..models import expense_model

router = APIRouter()


@router.get(
    "/category_expense",
    summary="Get all expense based on categories",
    status_code=status.HTTP_200_OK,
    # response_model=schemas.ExpenseCategory,
)
def get_category_expense(
    request: Request,
):
    try:
        category_expense = {}
        expenses = (
            expense_model.Expense.query()
            .filter(expense_model.Expense.created_by_id == request.state.user_id)
            .all()
        )
        for expense in expenses:
            category_expense[expense.category.name] = category_expense.get(
                expense.category.name, 0
            ) + abs(expense.amount)
        category_expense = [["Category", "Amount"]] + [
            [k, v] for k, v in category_expense.items()
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return category_expense
