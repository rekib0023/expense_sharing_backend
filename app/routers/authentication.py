from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app import oauth2, schemas, utils
from app.config import settings
from app.models import User
from app.oauth2 import AuthJWT

router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post(
    "/signup",
    summary="Create new user",
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    payload: schemas.CreateUserSchema,
    response: Response,
    Authorize: AuthJWT = Depends(),
):
    user = User.get_by(email=payload.email.lower())
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exist",
        )
    user = {
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "email": payload.email,
        "hashed_password": utils.get_hashed_password(payload.password),
    }

    user = User.create(**user)

    access_token = Authorize.create_access_token(
        subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
    )

    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id),
        expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN),
    )

    response.set_cookie(
        "access_token",
        access_token,
        max_age=ACCESS_TOKEN_EXPIRES_IN * 60,
        expires=ACCESS_TOKEN_EXPIRES_IN * 60,
        secure=True,
        httponly=True,
        samesite=None,
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        max_age=REFRESH_TOKEN_EXPIRES_IN * 60,
        expires=REFRESH_TOKEN_EXPIRES_IN * 60,
        secure=False,
        httponly=True,
        samesite=None,
    )
    response.set_cookie(
        "logged_in",
        "True",
        max_age=ACCESS_TOKEN_EXPIRES_IN * 60,
        expires=ACCESS_TOKEN_EXPIRES_IN * 60,
        secure=False,
        httponly=False,
        samesite="lax",
    )

    return {"status": "success", "access_token": access_token}


@router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    status_code=status.HTTP_200_OK,
)
def login(
    payload: schemas.LoginUserSchema, response: Response, Authorize: AuthJWT = Depends()
):
    user = User.get_by(email=payload.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    hashed_pass = user.hashed_password
    if not utils.verify_password(payload.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    access_token = Authorize.create_access_token(
        subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN)
    )

    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id),
        expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN),
    )

    response.set_cookie(
        "access_token",
        access_token,
        max_age=ACCESS_TOKEN_EXPIRES_IN * 60,
        expires=ACCESS_TOKEN_EXPIRES_IN * 60,
        secure=True,
        httponly=True,
        samesite=None,
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        max_age=REFRESH_TOKEN_EXPIRES_IN * 60,
        expires=REFRESH_TOKEN_EXPIRES_IN * 60,
        secure=False,
        httponly=True,
        samesite=None,
    )
    response.set_cookie(
        "logged_in",
        "True",
        max_age=ACCESS_TOKEN_EXPIRES_IN * 60,
        expires=ACCESS_TOKEN_EXPIRES_IN * 60,
        secure=False,
        httponly=False,
        samesite="lax",
    )

    return {"status": "success", "access_token": access_token}


@router.get(
    "/refresh", summary="Get refreshed access token", status_code=status.HTTP_200_OK
)
def refresh_token(response: Response, request: Request, Authorize: AuthJWT = Depends()):
    try:
        print(Authorize._refresh_cookie_key)
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not refresh access token",
            )
        user = User.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user belonging to this token no logger exist",
            )
        access_token = Authorize.create_access_token(
            subject=str(user.id),
            expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN),
        )
    except Exception as e:
        error = e.__class__.__name__
        print(error)
        if error == "MissingTokenError":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in"
            )
        if error == "UserNotFound":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exist"
            )
        if error == "NotVerified":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please verify your account",
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or has expired",
        )

    response.set_cookie(
        "access_token",
        access_token,
        max_age=ACCESS_TOKEN_EXPIRES_IN * 60,
        expires=ACCESS_TOKEN_EXPIRES_IN * 60,
        secure=True,
        httponly=True,
        samesite=None,
    )
    response.set_cookie(
        "logged_in",
        "True",
        max_age=ACCESS_TOKEN_EXPIRES_IN * 60,
        expires=ACCESS_TOKEN_EXPIRES_IN * 60,
        secure=False,
        httponly=False,
        samesite="lax",
    )

    return {"access_token": access_token}


@router.get("/logout", status_code=status.HTTP_200_OK)
def logout(
    response: Response,
    Authorize: AuthJWT = Depends(),
    _: str = Depends(oauth2.require_user),
):
    Authorize.unset_jwt_cookies()
    response.set_cookie("logged_in", "", -1)

    return {"status": "success"}
