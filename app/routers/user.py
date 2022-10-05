from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas

router = APIRouter()


@router.get("/me", response_model=schemas.UserResponse)
def get_me(user_id: str = Depends(oauth2.require_user)):
    user = models.User.get(user_id)
    return user


@router.get("/all")
def get_me(_: str = Depends(oauth2.require_user)):
    users = models.User.query().all()
    user_list = [
        schemas.UserResponse(**user.as_dict()) for user in users
    ]
    return user_list
