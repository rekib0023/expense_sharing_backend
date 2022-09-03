from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2

router = APIRouter()


@router.get('/me', response_model=schemas.UserResponse)
def get_me(user_email: str = Depends(oauth2.require_user)):
    user = models.User.get_by(email=user_email)
    return user