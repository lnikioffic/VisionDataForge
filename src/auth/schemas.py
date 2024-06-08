from pydantic import BaseModel, EmailStr
from fastapi import Form


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = 'Bearer'


class AuthForm(BaseModel):
    username: str = Form()
    # email: EmailStr = Form()
    password: str = Form()
