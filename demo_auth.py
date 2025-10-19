from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from schemas.user import UserSchema

from jwt.exceptions import InvalidTokenError

from auth import utils as auth_utils

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"

# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(
    "/jwt/login/",
)
#
from pydantic import BaseModel


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="/jwt", tags=["jwt"])

alex = UserSchema(
    username="alex228",
    password=auth_utils.hash_password("1234"),
    email="alex@alex.com",
)

users_db: dict[str, UserSchema] = {
    alex.username: alex,
}


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    # доствем user из базы
    if not (user := users_db.get(username)):
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password,
        hashed_pwd=user.password,
    ):
        raise unauthed_exc

    return user


@router.post("/login/")
def auth_user(user: UserSchema = Depends(validate_auth_user)):
    jwt_payload = {
        "type": "access",
        # sub
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


def get_current_token_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> dict:
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
        )
    return payload


def get_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    # замени на константы
    token_type = payload.get(TOKEN_TYPE_FIELD)
    if token_type != ACCESS_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token type '{token_type}' expected '{ACCESS_TOKEN_TYPE}'",
        )
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )


@router.get("users/me/")
def auth_user_check_self_info(user: UserSchema = Depends(get_auth_user)):
    return {
        "username": user.username,
        "email": user.email,
    }
