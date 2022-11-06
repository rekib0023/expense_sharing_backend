from fastapi import APIRouter, Depends, Request

from .. import oauth2, schemas
from ..models import expense_model

router = APIRouter()


@router.get("/me", response_model=schemas.UserResponse)
def get_me(
    request: Request,
):
    user = expense_model.User.get(request.state.user_id)
    return user


@router.get("/all")
def get_all(
    request: Request,
):
    users = expense_model.User.query().all()
    user_list = [schemas.UserResponse(**user.as_dict()) for user in users]
    return user_list
